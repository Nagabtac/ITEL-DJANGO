from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('addStudent', views.addStudent),
    path('deleteStudent', views.deleteStudent),
    path('updatePage', views.updatePage),
    path('updateInfo', views.updateInfo),
    
    # Authentication API endpoints
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/profile/', views.user_profile_api, name='user_profile_api'),
    
    # Todo API endpoints (require authentication)
    path('api/todos/', views.todo_api, name='todo_api'),
    path('api/todos/<int:todo_id>/', views.todo_detail_api, name='todo_detail_api'),
]