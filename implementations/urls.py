from django.urls import path
from .views import index, submit_implementation_view, graph_view, about_view, terms_view, privacy_view, cookies_policy_view

urlpatterns = [
    path('', index, name='index'),
    path('submit/', submit_implementation_view, name='submit'),
    path('graphs/', graph_view, name='graphs'),
    path('about/', about_view, name='about'),
    path('terms/', terms_view, name='terms'),
    path('pricacy/', privacy_view, name='privacy'),
    path('cookies-policy/', cookies_policy_view, name='cookies-policy'),
]
