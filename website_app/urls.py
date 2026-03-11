from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('addStudent', views.addStudent),
    path('deleteStudent', views.deleteStudent),
    path('updatePage', views.updatePage),
    path('updateInfo', views.updateInfo),
]