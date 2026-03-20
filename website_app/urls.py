from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('addStudent', views.addStudent),
    path('deleteStudent', views.deleteStudent),
    path('updatePage', views.updatePage),
    path('updateInfo', views.updateInfo),
    
    # Todo API endpoints only (React frontend)
    path('api/todos/', views.todo_api, name='todo_api'),
    path('api/todos/<int:todo_id>/', views.todo_detail_api, name='todo_detail_api'),
]