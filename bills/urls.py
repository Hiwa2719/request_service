from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'bills'

router = DefaultRouter()
router.register('bills', views.BillViewSet, basename='bills')

urlpatterns = [
    path('<int:user_id>/', views.get_user_bills, name='user-bills')
]

urlpatterns += router.urls
