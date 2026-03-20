from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
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

def add_cors_headers(request, response):
    """Add CORS headers to response"""
    # Must not be '*' when Allow-Credentials is enabled, otherwise browsers
    # block credentialed requests (cookies/session). Echo the request origin
    # for local dev.
    origin = request.headers.get('Origin') if request else None
    response['Access-Control-Allow-Origin'] = origin or 'http://localhost:3000'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


# AUTHENTICATION API ENDPOINTS

@csrf_exempt
def register_api(request):
    """API endpoint for user registration"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(request, response)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '')
            email = data.get('email', '').strip()
            
            # Validation
            if not username or not password:
                response = JsonResponse({'error': 'Username and password are required'}, status=400)
                return add_cors_headers(request, response)
            
            if len(password) < 6:
                response = JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)
                return add_cors_headers(request, response)
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                response = JsonResponse({'error': 'Username already exists'}, status=400)
                return add_cors_headers(request, response)
            
            # Create user with hashed password
            user = User.objects.create_user(
                username=username,
                password=password,  # Django automatically hashes this
                email=email
            )
            
            response = JsonResponse({
                'message': 'User registered successfully',
                'user_id': user.id,
                'username': user.username
            }, status=201)
            return add_cors_headers(request, response)
            
        except json.JSONDecodeError:
            response = JsonResponse({'error': 'Invalid JSON'}, status=400)
            return add_cors_headers(request, response)
    
    response = JsonResponse({'error': 'Method not allowed'}, status=405)
    return add_cors_headers(request, response)


@csrf_exempt
def login_api(request):
    """API endpoint for user login"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(request, response)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                response = JsonResponse({'error': 'Username and password are required'}, status=400)
                return add_cors_headers(request, response)
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                response = JsonResponse({
                    'message': 'Login successful',
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                })
                return add_cors_headers(request, response)
            else:
                response = JsonResponse({'error': 'Invalid username or password'}, status=401)
                return add_cors_headers(request, response)
                
        except json.JSONDecodeError:
            response = JsonResponse({'error': 'Invalid JSON'}, status=400)
            return add_cors_headers(request, response)
    
    response = JsonResponse({'error': 'Method not allowed'}, status=405)
    return add_cors_headers(request, response)


@csrf_exempt
def logout_api(request):
    """API endpoint for user logout"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(request, response)
    
    if request.method == "POST":
        logout(request)
        response = JsonResponse({'message': 'Logout successful'})
        return add_cors_headers(request, response)
    
    response = JsonResponse({'error': 'Method not allowed'}, status=405)
    return add_cors_headers(request, response)


@csrf_exempt
def user_profile_api(request):
    """API endpoint to get current user profile"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(request, response)
    
    if request.method == "GET":
        if request.user.is_authenticated:
            response = JsonResponse({
                'user_id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'is_authenticated': True
            })
            return add_cors_headers(request, response)
        else:
            response = JsonResponse({'is_authenticated': False}, status=401)
            return add_cors_headers(request, response)
    
    response = JsonResponse({'error': 'Method not allowed'}, status=405)
    return add_cors_headers(request, response)


@csrf_exempt
def todo_api(request):
    """API endpoint for todos - GET all todos or POST new todo"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(request, response)
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        response = JsonResponse({'error': 'Authentication required'}, status=401)
        return add_cors_headers(request, response)
    
    if request.method == "GET":
        todos = Todo.objects.filter(user=request.user)
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
        return add_cors_headers(request, response)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            todo = Todo.objects.create(
                user=request.user,
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
            return add_cors_headers(request, response)
        except json.JSONDecodeError:
            response = JsonResponse({'error': 'Invalid JSON'}, status=400)
            return add_cors_headers(request, response)


@csrf_exempt
def todo_detail_api(request, todo_id):
    """API endpoint for individual todo - PUT to update or DELETE"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(request, response)
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        response = JsonResponse({'error': 'Authentication required'}, status=401)
        return add_cors_headers(request, response)
    
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
    except Todo.DoesNotExist:
        response = JsonResponse({'error': 'Todo not found'}, status=404)
        return add_cors_headers(request, response)
    
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
            return add_cors_headers(request, response)
        except json.JSONDecodeError:
            response = JsonResponse({'error': 'Invalid JSON'}, status=400)
            return add_cors_headers(request, response)
    
    elif request.method == "DELETE":
        todo.delete()
        response = JsonResponse({'message': 'Todo deleted successfully'}, status=204)
        return add_cors_headers(request, response)