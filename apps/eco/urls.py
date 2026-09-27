from django.urls import path
from .views import rainwater_calculator

urlpatterns = [
path("", rainwater_calculator, name="rainwater_calculator"),
]