from django.urls import path
from . import views

app_name= 'bills'

urlpatterns = [
    path('<int:user_id>/', views.get_user_bills, name='user-bills')
]