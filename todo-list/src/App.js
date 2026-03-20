import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import AuthForm from './components/AuthForm';

const API_BASE_URL = 'http://localhost:8000/api/todos/';

// Ensure Django session cookies are sent/received cross-origin
axios.defaults.withCredentials = true;

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      loadTodos();
    }
  }, [isAuthenticated]);

  const checkAuthStatus = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/profile/', { withCredentials: true });
      if (response.data.is_authenticated) {
        setUser(response.data);
        setIsAuthenticated(true);
      }
    } catch (err) {
      setIsAuthenticated(false);
    } finally {
      setCheckingAuth(false);
    }
  };

  const handleAuthSuccess = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
    setError('');
  };

  const handleLogout = async () => {
    try {
      await axios.post('http://localhost:8000/api/logout/', {}, { withCredentials: true });
      setUser(null);
      setIsAuthenticated(false);
      setTodos([]);
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  const loadTodos = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(API_BASE_URL, { withCredentials: true });
      setTodos(response.data.todos);
    } catch (err) {
      if (err.response?.status === 401) {
        setIsAuthenticated(false);
        setUser(null);
      } else {
        setError('Failed to load todos: ' + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (todoData) => {
    try {
      const response = await axios.post(API_BASE_URL, todoData, { withCredentials: true });
      setTodos([response.data, ...todos]);
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        setIsAuthenticated(false);
        setUser(null);
      } else {
        setError('Failed to add todo: ' + err.message);
      }
    }
  };

  const toggleTodo = async (id, completed) => {
    try {
      await axios.put(`${API_BASE_URL}${id}/`, {
        completed: !completed
      }, { withCredentials: true });
      setTodos(todos.map(todo => 
        todo.id === id ? { ...todo, completed: !completed } : todo
      ));
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        setIsAuthenticated(false);
        setUser(null);
      } else {
        setError('Failed to update todo: ' + err.message);
      }
    }
  };

  const deleteTodo = async (id) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    try {
      await axios.delete(`${API_BASE_URL}${id}/`, { withCredentials: true });
      setTodos(todos.filter(todo => todo.id !== id));
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        setIsAuthenticated(false);
        setUser(null);
      } else {
        setError('Failed to delete todo: ' + err.message);
      }
    }
  };

  if (checkingAuth) {
    return (
      <div className="App">
        <div className="loading">Checking authentication...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthForm onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <h1>Todo List</h1>
          <div className="user-info">
            <span>Welcome, {user?.username}!</span>
            <button className="btn btn-secondary" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
        
        <TodoForm onAddTodo={addTodo} />
        
        {error && <div className="error">{error}</div>}
        
        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <TodoList 
            todos={todos}
            onToggleTodo={toggleTodo}
            onDeleteTodo={deleteTodo}
          />
        )}
      </div>
    </div>
  );
}

export default App;