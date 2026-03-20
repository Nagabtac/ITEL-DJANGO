import React from 'react';
import TodoItem from './TodoItem';
import './TodoList.css';

const TodoList = ({ todos, onToggleTodo, onDeleteTodo }) => {
  if (todos.length === 0) {
    return (
      <div className="empty-state">
        <h3>No todos yet!</h3>
        <p>Add your first todo above to get started.</p>
      </div>
    );
  }

  return (
    <div className="todo-list">
      <h3>Your Todos ({todos.length})</h3>
      <div className="todos-container">
        {todos.map(todo => (
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggle={() => onToggleTodo(todo.id, todo.completed)}
            onDelete={() => onDeleteTodo(todo.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default TodoList;