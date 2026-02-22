from django.shortcuts import render


def index(request):
	return render(request, 'home/index.html')


def privacy_policy(request):
	return render(request, 'home/privacy.html')


def cookie_policy(request):
	return render(request, 'home/cookie.html')


def terms_conditions(request):
	return render(request, 'home/terms.html')
