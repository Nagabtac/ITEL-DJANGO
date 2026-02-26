from django.urls import path
from . import views  # Import your views here

urlpatterns = [
    # Do NOT use include() here to point to this same file or the project file
    path('', views.student_list, name='student_list'), 
    # ... other paths ...
]