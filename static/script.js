const API_BASE = '/api';

// Load stats and tasks on page load
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadTasks();
    setupEventListeners();
});

function setupEventListeners() {
    // Task creation form
    document.getElementById('taskForm').addEventListener('submit', createTask);

    // Task editing form
    document.getElementById('editTaskForm').addEventListener('submit', updateTask);

    // Filters
    document.getElementById('statusFilter').addEventListener('change', loadTasks);
    document.getElementById('priorityFilter').addEventListener('change', loadTasks);

    // Modal
    const modal = document.getElementById('editModal');
    const closeBtn = document.querySelector('.close');

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const result = await response.json();

        if (result.success) {
            const stats = result.data;
            document.getElementById('totalTasks').textContent = stats.total_tasks;
            document.getElementById('completedTasks').textContent = stats.completed_tasks;
            document.getElementById('pendingTasks').textContent = stats.pending_tasks;
            document.getElementById('inProgressTasks').textContent = stats.in_progress_tasks;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadTasks() {
    const loading = document.getElementById('loading');
    const tasksGrid = document.getElementById('tasksGrid');

    loading.style.display = 'block';
    tasksGrid.innerHTML = '';

    try {
        const statusFilter = document.getElementById('statusFilter').value;
        const priorityFilter = document.getElementById('priorityFilter').value;

        let url = `${API_BASE}/tasks`;
        const params = new URLSearchParams();

        if (statusFilter) params.append('status', statusFilter);
        if (priorityFilter) params.append('priority', priorityFilter);

        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await fetch(url);
        const result = await response.json();

        loading.style.display = 'none';

        if (result.success) {
            displayTasks(result.data);
        } else {
            showNotification('Error loading tasks: ' + result.error, 'error');
        }
    } catch (error) {
        loading.style.display = 'none';
        showNotification('Error loading tasks: ' + error.message, 'error');
    }
}

function displayTasks(tasks) {
    const tasksGrid = document.getElementById('tasksGrid');

    if (tasks.length === 0) {
        tasksGrid.innerHTML = '<p style="text-align: center; color: #666; font-size: 1.1rem; padding: 40px;">No tasks found. Create your first task above! 🎯</p>';
        return;
    }

    tasksGrid.innerHTML = tasks.map(task => `
        <div class="task-card">
            <div class="task-title">${escapeHtml(task.title)}</div>
            <div class="task-meta">
                <span class="badge badge-status ${task.status}">${task.status.replace('_', ' ')}</span>
                <span class="badge badge-priority ${task.priority}">${task.priority}</span>
                ${task.assigned_to ? `<span class="badge" style="background: #f0f0f0; color: #333;">👤 ${escapeHtml(task.assigned_to)}</span>` : ''}
                ${task.due_date ? `<span class="badge" style="background: #fff3cd; color: #856404;">📅 ${new Date(task.due_date).toLocaleDateString()}</span>` : ''}
            </div>
            ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
            <div class="task-actions">
                <button class="btn btn-small" onclick="editTask('${task._id}')">✏️ Edit</button>
                <button class="btn btn-danger btn-small" onclick="deleteTask('${task._id}')">🗑️ Delete</button>
            </div>
        </div>
    `).join('');
}

async function createTask(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const taskData = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });

        const result = await response.json();

        if (result.success) {
            showNotification('Task created successfully! 🎉', 'success');
            event.target.reset();
            loadTasks();
            loadStats();
        } else {
            showNotification('Error creating task: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error creating task: ' + error.message, 'error');
    }
}

async function editTask(taskId) {
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`);
        const result = await response.json();

        if (result.success) {
            const task = result.data;

            // Populate edit form
            document.getElementById('editTaskId').value = task._id;
            document.getElementById('editTitle').value = task.title;
            document.getElementById('editStatus').value = task.status;
            document.getElementById('editPriority').value = task.priority;
            document.getElementById('editAssignedTo').value = task.assigned_to || '';
            document.getElementById('editDueDate').value = task.due_date ? task.due_date.split('T')[0] : '';
            document.getElementById('editDescription').value = task.description || '';

            // Show modal
            document.getElementById('editModal').style.display = 'block';
        } else {
            showNotification('Error loading task: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error loading task: ' + error.message, 'error');
    }
}

async function updateTask(event) {
    event.preventDefault();

    const taskId = document.getElementById('editTaskId').value;
    const formData = new FormData(event.target);
    const taskData = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });

        const result = await response.json();

        if (result.success) {
            showNotification('Task updated successfully! ✅', 'success');
            document.getElementById('editModal').style.display = 'none';
            loadTasks();
            loadStats();
        } else {
            showNotification('Error updating task: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error updating task: ' + error.message, 'error');
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.success) {
            showNotification('Task deleted successfully! 🗑️', 'success');
            loadTasks();
            loadStats();
        } else {
            showNotification('Error deleting task: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error deleting task: ' + error.message, 'error');
    }
}

function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;