import React from 'react';
import './TodoItem.css';

const TodoItem = ({ todo, onToggle, onDelete }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        <div className="todo-header">
          <h4 className={`todo-title ${todo.completed ? 'completed' : ''}`}>
            {todo.title}
          </h4>
          <div className="todo-meta">
            <span className="todo-date">
              Created: {formatDate(todo.created_at)}
            </span>
            {todo.updated_at !== todo.created_at && (
              <span className="todo-date">
                Updated: {formatDate(todo.updated_at)}
              </span>
            )}
          </div>
        </div>
        
        {todo.description && (
          <p className="todo-description">{todo.description}</p>
        )}
      </div>
      
      <div className="todo-actions">
        <button
          className={`btn ${todo.completed ? 'btn-secondary' : 'btn-success'}`}
          onClick={onToggle}
        >
          {todo.completed ? 'Undo' : 'Complete'}
        </button>
        <button
          className="btn btn-danger"
          onClick={onDelete}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TodoItem;