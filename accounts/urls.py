from .views import register_view, login_view, logout_view, update_account_view
from django.urls import path

urlpatterns = [
    path('register', register_view, name="register"),
    path('update', update_account_view, name="update"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
]