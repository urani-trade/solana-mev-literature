from django.urls import path, include
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, register_view

"""
Add all accounts and password reset URLs. 
Note that we are using django.contrib.auth's views 
so to have the views working we need a directory 
named register/ and we need a reverse login named 
`signin`.
"""

urlpatterns = [
    path('login/', login_view, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    url('^', include('django.contrib.auth.urls')),
    path('login/', login_view, name='login'),
]
