from urllib.parse import urlencode
from time import time
from types import SimpleNamespace

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Max
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Answer, Question, Test, TestResult

from .forms import AnswerForm, QuestionForm, TestForm


GUEST_RESULT_SESSION_KEY = "assessments_guest_result"


def test_list(request):
    tests = Test.objects.filter(is_active=True).order_by("title")
    return render(
        request,
        "assessments/tests_list.html",
        {
            "tests": tests,
            "is_guest": not request.user.is_authenticated,
        },
    )


def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, is_active=True)
    questions = list(test.questions.prefetch_related("answers").all())
    total_questions = len(questions)

    if not total_questions:
        return render(
            request,
            "assessments/take_test.html",
            {
                "test": test,
                "questions": [],
                "is_guest": not request.user.is_authenticated,
            },
        )

    session_key = "assessments_test_wizard"
    wizard_state = request.session.get(session_key, {})
    test_state = wizard_state.get(str(test.id), {"index": 0, "answers": {}})
    current_index = max(0, min(int(test_state.get("index", 0) or 0), total_questions - 1))
    answers_map = test_state.get("answers", {}) if isinstance(test_state.get("answers", {}), dict) else {}

    if request.method == "POST":
        is_guest = not request.user.is_authenticated
        current_question = questions[current_index]
        answer_id = request.POST.get(f"question_{current_question.id}")

        if not answer_id:
            return render(
                request,
                "assessments/take_test.html",
                {
                    "test": test,
                    "questions": questions,
                    "current_question": current_question,
                    "current_step": current_index + 1,
                    "total_steps": total_questions,
                    "progress_percent": int(((current_index + 1) / total_questions) * 100),
                    "selected_answer_id": None,
                    "error_message": "Seleziona una risposta per continuare.",
                    "is_guest": is_guest,
                    "is_final_step": current_index == total_questions - 1,
                },
            )

        answer = current_question.answers.filter(id=answer_id).first()
        if not answer:
            return render(
                request,
                "assessments/take_test.html",
                {
                    "test": test,
                    "questions": questions,
                    "current_question": current_question,
                    "current_step": current_index + 1,
                    "total_steps": total_questions,
                    "progress_percent": int(((current_index + 1) / total_questions) * 100),
                    "selected_answer_id": None,
                    "error_message": "La risposta selezionata non è valida.",
                    "is_guest": is_guest,
                    "is_final_step": current_index == total_questions - 1,
                },
            )

        answers_map[str(current_question.id)] = answer.id
        test_state["answers"] = answers_map
        wizard_state[str(test.id)] = test_state
        request.session[session_key] = wizard_state
        request.session.modified = True

        if current_index < total_questions - 1:
            test_state["index"] = current_index + 1
            wizard_state[str(test.id)] = test_state
            request.session[session_key] = wizard_state
            request.session.modified = True
            return redirect("assessments:take-test", test_id=test.id)

        if is_guest and request.POST.get("guest_consent") != "on":
            return render(
                request,
                "assessments/take_test.html",
                {
                    "test": test,
                    "questions": questions,
                    "current_question": current_question,
                    "current_step": current_index + 1,
                    "total_steps": total_questions,
                    "progress_percent": int(((current_index + 1) / total_questions) * 100),
                    "selected_answer_id": answer.id,
                    "error_message": "Per continuare come ospite devi accettare Privacy e Cookie Policy.",
                    "is_guest": True,
                    "is_final_step": True,
                },
            )

        total_score = 0
        missing_answers = []
        for question in questions:
            selected_id = answers_map.get(str(question.id))
            selected_answer = question.answers.filter(id=selected_id).first()
            if not selected_answer:
                missing_answers.append(question.id)
                continue
            total_score += selected_answer.points

        if missing_answers:
            test_state["index"] = 0
            test_state["answers"] = {}
            wizard_state[str(test.id)] = test_state
            request.session[session_key] = wizard_state
            request.session.modified = True
            return redirect("assessments:take-test", test_id=test.id)

        if is_guest and _is_guest_rate_limited(request):
            return render(
                request,
                "assessments/take_test.html",
                {
                    "test": test,
                    "questions": questions,
                    "current_question": current_question,
                    "current_step": current_index + 1,
                    "total_steps": total_questions,
                    "progress_percent": int(((current_index + 1) / total_questions) * 100),
                    "selected_answer_id": answer.id,
                    "error_message": "Hai effettuato troppi invii in poco tempo. Riprova tra un minuto.",
                    "is_guest": True,
                    "is_final_step": True,
                },
            )

        personality = test.get_personality_for_score(total_score)

        if request.user.is_authenticated:
            result = TestResult.objects.create(
                user=request.user,
                test=test,
                score=total_score,
                personality=personality,
            )
        else:
            request.session[GUEST_RESULT_SESSION_KEY] = {
                "test_id": test.id,
                "test_title": test.title,
                "score": total_score,
                "personality_id": personality.id if personality else None,
                "personality_name": personality.name if personality else "",
                "personality_description": personality.description if personality else "",
            }
            request.session.modified = True

        wizard_state = request.session.get(session_key, {})
        wizard_state.pop(str(test.id), None)
        request.session[session_key] = wizard_state
        request.session.modified = True
        if request.user.is_authenticated:
            return redirect("assessments:test-result", result_id=result.id)
        return redirect("assessments:guest-test-result")

    current_question = questions[current_index]
    selected_answer_id = answers_map.get(str(current_question.id))
    return render(
        request,
        "assessments/take_test.html",
        {
            "test": test,
            "questions": questions,
            "current_question": current_question,
            "current_step": current_index + 1,
            "total_steps": total_questions,
            "progress_percent": int(((current_index + 1) / total_questions) * 100),
            "selected_answer_id": selected_answer_id,
            "is_final_step": current_index == total_questions - 1,
            "is_guest": not request.user.is_authenticated,
        },
    )


def test_result(request, result_id):
    result = get_object_or_404(TestResult, id=result_id)

    if not request.user.is_authenticated or result.user_id != request.user.id:
        login_url = f"{reverse('account_login')}?{urlencode({'next': request.path})}"
        return redirect(login_url)

    return render(
        request,
        "assessments/test_result.html",
        {
            "result": result,
            "is_guest_result": False,
        },
    )


def guest_test_result(request):
    payload = request.session.get(GUEST_RESULT_SESSION_KEY)
    if not payload:
        return redirect("assessments:tests-list")

    if request.user.is_authenticated:
        test = Test.objects.filter(id=payload.get("test_id"), is_active=True).first()
        if not test:
            request.session.pop(GUEST_RESULT_SESSION_KEY, None)
            request.session.modified = True
            return redirect("assessments:tests-list")

        personality_id = payload.get("personality_id")
        personality = test.personalities.filter(id=personality_id).first() if personality_id else None

        result = TestResult.objects.create(
            user=request.user,
            test=test,
            score=int(payload.get("score") or 0),
            personality=personality,
        )
        request.session.pop(GUEST_RESULT_SESSION_KEY, None)
        request.session.modified = True
        return redirect("assessments:test-result", result_id=result.id)

    result = SimpleNamespace(
        score=int(payload.get("score") or 0),
        test=SimpleNamespace(title=payload.get("test_title") or "Test"),
        personality=(
            SimpleNamespace(
                name=payload.get("personality_name") or "",
                description=payload.get("personality_description") or "",
            )
            if payload.get("personality_name")
            else None
        ),
    )

    return render(
        request,
        "assessments/test_result.html",
        {
            "result": result,
            "is_guest_result": True,
        },
    )

def _is_guest_rate_limited(request):
    limit = getattr(settings, "ASSESSMENTS_GUEST_RATE_LIMIT_COUNT", 5)
    window_seconds = getattr(settings, "ASSESSMENTS_GUEST_RATE_LIMIT_WINDOW_SECONDS", 60)
    now_ts = int(time())

    session_key = "assessments_guest_submit_timestamps"
    recent = [ts for ts in request.session.get(session_key, []) if now_ts - ts < window_seconds]
    if len(recent) >= limit:
        request.session[session_key] = recent
        return True

    recent.append(now_ts)
    request.session[session_key] = recent
    return False


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
