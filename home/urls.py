from django.urls import path

from .views import cookie_policy, index, privacy_policy, terms_conditions

urlpatterns = [
    path('', index, name='home-index'),
    path('privacy/', privacy_policy, name='privacy-policy'),
    path('cookie/', cookie_policy, name='cookie-policy'),
    path('terms/', terms_conditions, name='terms-conditions'),
]
