from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('result/<int:analysis_id>/', views.analysis_result, name='analysis_result'),
]