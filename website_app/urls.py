from django.urls import path
from website_app import views

urlpatterns = [
    path('', views.index)
]