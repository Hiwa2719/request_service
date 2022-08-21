from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_email, name='activate-email'),
    path('change-password/', views.change_password, name='change-password'),
]
