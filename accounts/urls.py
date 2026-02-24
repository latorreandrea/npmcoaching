from django.urls import path

from .views import admin_dashboard, profile, take_test, test_list, test_result

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('dashboard/', admin_dashboard, name='admin-dashboard'),
    path('tests/', test_list, name='tests-list'),
    path('tests/<int:test_id>/', take_test, name='take-test'),
    path('tests/results/<int:result_id>/', test_result, name='test-result'),
]
