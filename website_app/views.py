from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Student, Todo


# READ
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


# CREATE
def addStudent(request):
    if request.method == "POST":
        name = request.POST['name']
        course = request.POST['course']
        motto = request.POST['motto']

        Student.objects.create(
            name=name,
            course=course,
            motto=motto
        )
        return redirect('student_list')


# DELETE
def deleteStudent(request):
    if request.method == "POST":
        id = request.POST['id']
        student = Student.objects.get(id=id)
        student.delete()
        return redirect('student_list')


# OPEN UPDATE PAGE
def updatePage(request):
    if request.method == "POST":
        id = request.POST['id']
        student = Student.objects.get(id=id)
        return render(request, 'students/update.html', {'student': student})


# UPDATE DATA
def updateInfo(request):
    if request.method == "POST":
        id = request.POST['id']
        student = Student.objects.get(id=id)

        student.name = request.POST['newName']
        student.course = request.POST['newCourse']
        student.motto = request.POST['newMotto']
        student.save()

        return redirect('student_list')


# TODO API ENDPOINTS

def add_cors_headers(response):
    """Add CORS headers to response"""
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@csrf_exempt
def todo_api(request):
    """API endpoint for todos - GET all todos or POST new todo"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    
    if request.method == "GET":
        todos = Todo.objects.all()
        todo_list = []
        for todo in todos:
            todo_list.append({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'completed': todo.completed,
                'created_at': todo.created_at.isoformat(),
                'updated_at': todo.updated_at.isoformat()
            })
        response = JsonResponse({'todos': todo_list})
        return add_cors_headers(response)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            todo = Todo.objects.create(
                title=data.get('title', ''),
                description=data.get('description', ''),
                completed=data.get('completed', False)
            )
            response = JsonResponse({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'completed': todo.completed,
                'created_at': todo.created_at.isoformat(),
                'updated_at': todo.updated_at.isoformat()
            }, status=201)
            return add_cors_headers(response)
        except json.JSONDecodeError:
            response = JsonResponse({'error': 'Invalid JSON'}, status=400)
            return add_cors_headers(response)


@csrf_exempt
def todo_detail_api(request, todo_id):
    """API endpoint for individual todo - PUT to update or DELETE"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        response = JsonResponse({'error': 'Todo not found'}, status=404)
        return add_cors_headers(response)
    
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            todo.title = data.get('title', todo.title)
            todo.description = data.get('description', todo.description)
            todo.completed = data.get('completed', todo.completed)
            todo.save()
            
            response = JsonResponse({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'completed': todo.completed,
                'created_at': todo.created_at.isoformat(),
                'updated_at': todo.updated_at.isoformat()
            })
            return add_cors_headers(response)
        except json.JSONDecodeError:
            response = JsonResponse({'error': 'Invalid JSON'}, status=400)
            return add_cors_headers(response)
    
    elif request.method == "DELETE":
        todo.delete()
        response = JsonResponse({'message': 'Todo deleted successfully'}, status=204)
        return add_cors_headers(response)