from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


@login_required
def profile(request):
	return render(request, 'accounts/profile.html')


@login_required
@user_passes_test(lambda user: user.is_staff)
def admin_dashboard(request):
	return render(request, 'accounts/admin_dashboard.html')
