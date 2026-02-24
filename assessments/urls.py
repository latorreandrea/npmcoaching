from django.urls import path

from .views import admin_test_builder, take_test, test_list, test_result

urlpatterns = [
    path("tests/", test_list, name="tests-list"),
    path("tests/<int:test_id>/", take_test, name="take-test"),
    path("tests/results/<int:result_id>/", test_result, name="test-result"),
    path("dashboard/test-builder/", admin_test_builder, name="admin-test-builder"),
]
