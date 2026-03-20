import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';

const API_BASE_URL = 'http://localhost:8000/api/todos/';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(API_BASE_URL);
      setTodos(response.data.todos);
    } catch (err) {
      setError('Failed to load todos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (todoData) => {
    try {
      const response = await axios.post(API_BASE_URL, todoData);
      setTodos([response.data, ...todos]);
      setError('');
    } catch (err) {
      setError('Failed to add todo: ' + err.message);
    }
  };

  const toggleTodo = async (id, completed) => {
    try {
      await axios.put(`${API_BASE_URL}${id}/`, {
        completed: !completed
      });
      setTodos(todos.map(todo => 
        todo.id === id ? { ...todo, completed: !completed } : todo
      ));
      setError('');
    } catch (err) {
      setError('Failed to update todo: ' + err.message);
    }
  };

  const deleteTodo = async (id) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    try {
      await axios.delete(`${API_BASE_URL}${id}/`);
      setTodos(todos.filter(todo => todo.id !== id));
      setError('');
    } catch (err) {
      setError('Failed to delete todo: ' + err.message);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Todo List</h1>
        
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