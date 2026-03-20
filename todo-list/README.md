# Todo List React Frontend

This is a React.js frontend that connects to your Django backend API.

## Setup Instructions

1. **Install Node.js dependencies:**
   ```bash
   cd todo-list
   npm install
   ```

2. **Install Django CORS headers (if not already installed):**
   ```bash
   pip install django-cors-headers
   ```

3. **Start the Django backend (in the main project directory):**
   ```bash
   python manage.py runserver
   ```

4. **Start the React frontend (in a new terminal, from the todo-list directory):**
   ```bash
   npm start
   ```

## Access Points

- **React Frontend:** http://localhost:3000
- **Django Backend:** http://localhost:8000
- **Django Todo API:** http://localhost:8000/api/todos/
- **Django Admin:** http://localhost:8000/admin/

## Features

- ✅ Add new todos with title and description
- ✅ Mark todos as complete/incomplete
- ✅ Delete todos
- ✅ Real-time updates with Django backend
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states

## API Endpoints Used

- `GET /api/todos/` - Fetch all todos
- `POST /api/todos/` - Create new todo
- `PUT /api/todos/<id>/` - Update todo
- `DELETE /api/todos/<id>/` - Delete todo

## Technologies

- **Frontend:** React.js, Axios, CSS3
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL (as configured in Django settings)