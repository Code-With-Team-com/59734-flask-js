// API Base URL
const API_URL = '/api/tasks';

// DOM Elements
const taskForm = document.getElementById('taskForm');
const taskTitleInput = document.getElementById('taskTitle');
const taskDescriptionInput = document.getElementById('taskDescription');
const taskContainer = document.getElementById('taskContainer');

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    taskForm.addEventListener('submit', handleFormSubmit);
}

// Load all tasks from the API
async function loadTasks() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('Failed to fetch tasks');
        }
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
        showError('Failed to load tasks. Please refresh the page.');
    }
}

// Render tasks to the DOM
function renderTasks(tasks) {
    if (tasks.length === 0) {
        taskContainer.innerHTML = '<p class="empty-state">No tasks yet. Create your first task above!</p>';
        return;
    }

    taskContainer.innerHTML = tasks.map(task => createTaskHTML(task)).join('');
    attachTaskEventListeners();
}

// Create HTML for a single task
function createTaskHTML(task) {
    const completedClass = task.completed ? 'completed' : '';
    const checkedAttr = task.completed ? 'checked' : '';
    const description = task.description ? `<p class="task-description">${escapeHtml(task.description)}</p>` : '';
    
    return `
        <div class="task-item ${completedClass}" data-id="${task.id}">
            <div class="task-checkbox">
                <input type="checkbox" ${checkedAttr} aria-label="Mark task as ${task.completed ? 'incomplete' : 'complete'}">
            </div>
            <div class="task-content">
                <h3 class="task-title">${escapeHtml(task.title)}</h3>
                ${description}
            </div>
            <div class="task-actions">
                <button class="btn btn-danger btn-sm delete-btn" aria-label="Delete task">Delete</button>
            </div>
        </div>
    `;
}

// Attach event listeners to task elements
function attachTaskEventListeners() {
    // Checkbox event listeners
    const checkboxes = document.querySelectorAll('.task-checkbox input');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleCheckboxChange);
    });

    // Delete button event listeners
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', handleDelete);
    });
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const title = taskTitleInput.value.trim();
    const description = taskDescriptionInput.value.trim();
    
    if (!title) {
        showError('Title is required');
        return;
    }
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, description })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create task');
        }
        
        // Clear form
        taskTitleInput.value = '';
        taskDescriptionInput.value = '';
        
        // Reload tasks
        loadTasks();
        showSuccess('Task created successfully!');
    } catch (error) {
        console.error('Error creating task:', error);
        showError(error.message);
    }
}

// Handle checkbox change (toggle completion)
async function handleCheckboxChange(event) {
    const taskItem = event.target.closest('.task-item');
    const taskId = taskItem.dataset.id;
    const completed = event.target.checked;
    
    try {
        const response = await fetch(`${API_URL}/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed })
        });
        
        if (!response.ok) {
            throw new Error('Failed to update task');
        }
        
        // Update UI
        if (completed) {
            taskItem.classList.add('completed');
        } else {
            taskItem.classList.remove('completed');
        }
    } catch (error) {
        console.error('Error updating task:', error);
        showError('Failed to update task');
        // Revert checkbox state
        event.target.checked = !completed;
    }
}

// Handle delete button click
async function handleDelete(event) {
    const taskItem = event.target.closest('.task-item');
    const taskId = taskItem.dataset.id;
    
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${taskId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete task');
        }
        
        // Remove from UI
        taskItem.remove();
        
        // Check if there are no more tasks
        const remainingTasks = document.querySelectorAll('.task-item');
        if (remainingTasks.length === 0) {
            taskContainer.innerHTML = '<p class="empty-state">No tasks yet. Create your first task above!</p>';
        }
        
        showSuccess('Task deleted successfully!');
    } catch (error) {
        console.error('Error deleting task:', error);
        showError('Failed to delete task');
    }
}

// Show success message
function showSuccess(message) {
    showFeedback(message, 'success');
}

// Show error message
function showError(message) {
    showFeedback(message, 'error');
}

// Show feedback message
function showFeedback(message, type) {
    // Remove existing feedback
    const existingFeedback = document.querySelector('.feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Create feedback element
    const feedback = document.createElement('div');
    feedback.className = `feedback ${type}`;
    feedback.textContent = message;
    
    // Insert at the top of the form
    const taskForm = document.querySelector('.task-form');
    taskForm.insertBefore(feedback, taskForm.firstChild);
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        feedback.remove();
    }, 3000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
