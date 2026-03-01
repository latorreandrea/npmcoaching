from django.urls import path

from .views import admin_test_builder, guest_test_result, take_test, test_list, test_result

urlpatterns = [
    path("tests/", test_list, name="tests-list"),
    path("tests/<int:test_id>/", take_test, name="take-test"),
    path("tests/results/guest/", guest_test_result, name="guest-test-result"),
    path("tests/results/<int:result_id>/", test_result, name="test-result"),
    path("dashboard/test-builder/", admin_test_builder, name="admin-test-builder"),
]
