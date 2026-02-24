from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .models import Test, TestResult


@login_required
def profile(request):
	return render(request, 'accounts/profile.html')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_dashboard(request):
	return render(request, 'accounts/admin_dashboard.html')


@login_required
def test_list(request):
	tests = Test.objects.filter(is_active=True).order_by('title')
	return render(request, 'accounts/tests_list.html', {'tests': tests})


@login_required
def take_test(request, test_id):
	test = get_object_or_404(Test, id=test_id, is_active=True)
	questions = test.questions.prefetch_related('answers').all()

	if request.method == 'POST':
		total_score = 0
		missing_questions = []

		for question in questions:
			answer_id = request.POST.get(f'question_{question.id}')
			if not answer_id:
				missing_questions.append(question.id)
				continue

			answer = question.answers.filter(id=answer_id).first()
			if answer:
				total_score += answer.points

		if missing_questions:
			return render(
				request,
				'accounts/take_test.html',
				{
					'test': test,
					'questions': questions,
					'error_message': 'Rispondi a tutte le domande prima di inviare il test.',
				},
			)

		personality = test.get_personality_for_score(total_score)
		result = TestResult.objects.create(
			user=request.user,
			test=test,
			score=total_score,
			personality=personality,
		)
		return redirect('accounts:test-result', result_id=result.id)

	return render(request, 'accounts/take_test.html', {'test': test, 'questions': questions})


@login_required
def test_result(request, result_id):
	result = get_object_or_404(TestResult, id=result_id, user=request.user)
	return render(request, 'accounts/test_result.html', {'result': result})
