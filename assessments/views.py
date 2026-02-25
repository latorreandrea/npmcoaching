from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Answer, Question, Test, TestResult

from .forms import AnswerForm, QuestionForm, TestForm


@login_required
def test_list(request):
    tests = Test.objects.filter(is_active=True).order_by("title")
    return render(request, "assessments/tests_list.html", {"tests": tests})


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, is_active=True)
    questions = test.questions.prefetch_related("answers").all()

    if request.method == "POST":
        total_score = 0
        missing_questions = []

        for question in questions:
            answer_id = request.POST.get(f"question_{question.id}")
            if not answer_id:
                missing_questions.append(question.id)
                continue

            answer = question.answers.filter(id=answer_id).first()
            if answer:
                total_score += answer.points

        if missing_questions:
            return render(
                request,
                "assessments/take_test.html",
                {
                    "test": test,
                    "questions": questions,
                    "error_message": "Rispondi a tutte le domande prima di inviare il test.",
                },
            )

        personality = test.get_personality_for_score(total_score)
        result = TestResult.objects.create(
            user=request.user,
            test=test,
            score=total_score,
            personality=personality,
        )
        return redirect("assessments:test-result", result_id=result.id)

    return render(request, "assessments/take_test.html", {"test": test, "questions": questions})


@login_required
def test_result(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    return render(request, "assessments/test_result.html", {"result": result})


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _builder_redirect(test_id=None, question_id=None, answer_id=None):
    base_url = reverse("assessments:admin-test-builder")
    params = {}
    if test_id:
        params["test"] = test_id
    if question_id:
        params["question"] = question_id
    if answer_id:
        params["answer"] = answer_id
    if not params:
        return redirect(base_url)
    return redirect(f"{base_url}?{urlencode(params)}")


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_test_builder(request):
    tests = Test.objects.all().order_by("title")
    selected_test = None
    selected_question = None
    selected_answer = None

    test_id = _safe_int(request.GET.get("test"))
    question_id = _safe_int(request.GET.get("question"))
    answer_id = _safe_int(request.GET.get("answer"))

    if test_id:
        selected_test = tests.filter(id=test_id).first()

    questions = Question.objects.none()
    if selected_test:
        questions = selected_test.questions.all()

    if question_id and selected_test:
        selected_question = questions.filter(id=question_id).first()

    answers = Answer.objects.none()
    if selected_question:
        answers = selected_question.answers.all()

    if answer_id and selected_question:
        selected_answer = answers.filter(id=answer_id).first()

    test_create_form = TestForm(prefix="test_create")
    test_edit_form = TestForm(instance=selected_test, prefix="test_edit") if selected_test else None
    question_create_form = QuestionForm(prefix="question_create") if selected_test else None
    question_edit_form = QuestionForm(instance=selected_question, prefix="question_edit") if selected_question else None
    answer_create_form = AnswerForm(prefix="answer_create") if selected_question else None
    answer_edit_form = AnswerForm(instance=selected_answer, prefix="answer_edit") if selected_answer else None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_test":
            test_create_form = TestForm(request.POST, prefix="test_create")
            if test_create_form.is_valid():
                new_test = test_create_form.save()
                return _builder_redirect(test_id=new_test.id)

        elif action == "update_test" and selected_test:
            test_edit_form = TestForm(request.POST, instance=selected_test, prefix="test_edit")
            if test_edit_form.is_valid():
                updated_test = test_edit_form.save()
                return _builder_redirect(test_id=updated_test.id)

        elif action == "delete_test" and selected_test:
            selected_test.delete()
            return _builder_redirect()

        elif action == "create_question" and selected_test:
            question_create_form = QuestionForm(request.POST, prefix="question_create")
            if question_create_form.is_valid():
                new_question = question_create_form.save(commit=False)
                new_question.test = selected_test
                max_order = selected_test.questions.aggregate(max_order=Max("order")).get("max_order") or 0
                new_question.order = max_order + 1
                new_question.save()
                return _builder_redirect(test_id=selected_test.id, question_id=new_question.id)

        elif action == "update_question" and selected_question:
            question_edit_form = QuestionForm(request.POST, instance=selected_question, prefix="question_edit")
            if question_edit_form.is_valid():
                updated_question = question_edit_form.save()
                return _builder_redirect(test_id=selected_test.id, question_id=updated_question.id)

        elif action == "delete_question" and selected_question:
            selected_question.delete()
            return _builder_redirect(test_id=selected_test.id)

        elif action == "reorder_questions" and selected_test:
            raw_ids = request.POST.get("ordered_question_ids", "")
            ordered_ids = [int(item) for item in raw_ids.split(",") if item.isdigit()]
            valid_ids = list(selected_test.questions.filter(id__in=ordered_ids).values_list("id", flat=True))
            if ordered_ids and len(valid_ids) == len(ordered_ids):
                for index, question_pk in enumerate(ordered_ids, start=1):
                    Question.objects.filter(id=question_pk, test=selected_test).update(order=index)
            return _builder_redirect(test_id=selected_test.id)

        elif action == "create_answer" and selected_question:
            answer_create_form = AnswerForm(request.POST, prefix="answer_create")
            if answer_create_form.is_valid():
                new_answer = answer_create_form.save(commit=False)
                new_answer.question = selected_question
                max_order = selected_question.answers.aggregate(max_order=Max("order")).get("max_order") or 0
                new_answer.order = max_order + 1
                new_answer.save()
                return _builder_redirect(test_id=selected_test.id, question_id=selected_question.id, answer_id=new_answer.id)

        elif action == "update_answer" and selected_answer:
            answer_edit_form = AnswerForm(request.POST, instance=selected_answer, prefix="answer_edit")
            if answer_edit_form.is_valid():
                updated_answer = answer_edit_form.save()
                return _builder_redirect(test_id=selected_test.id, question_id=selected_question.id, answer_id=updated_answer.id)

        elif action == "delete_answer" and selected_answer:
            selected_answer.delete()
            return _builder_redirect(test_id=selected_test.id, question_id=selected_question.id)

        elif action == "reorder_answers" and selected_question:
            raw_ids = request.POST.get("ordered_answer_ids", "")
            ordered_ids = [int(item) for item in raw_ids.split(",") if item.isdigit()]
            valid_ids = list(selected_question.answers.filter(id__in=ordered_ids).values_list("id", flat=True))
            if ordered_ids and len(valid_ids) == len(ordered_ids):
                for index, answer_pk in enumerate(ordered_ids, start=1):
                    Answer.objects.filter(id=answer_pk, question=selected_question).update(order=index)
            return _builder_redirect(test_id=selected_test.id, question_id=selected_question.id)

    context = {
        "tests": tests,
        "questions": questions,
        "answers": answers,
        "selected_test": selected_test,
        "selected_question": selected_question,
        "selected_answer": selected_answer,
        "test_create_form": test_create_form,
        "test_edit_form": test_edit_form,
        "question_create_form": question_create_form,
        "question_edit_form": question_edit_form,
        "answer_create_form": answer_create_form,
        "answer_edit_form": answer_edit_form,
    }
    return render(request, "assessments/admin_test_builder.html", context)
