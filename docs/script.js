const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    document.getElementById('taskForm').addEventListener('submit', createTask);
});

async function loadTasks() {
    const container = document.getElementById('tasksGrid');
    container.innerHTML = "Loading...";
    try {
        const res = await fetch(`${API_BASE}/tasks`);
        const data = await res.json();
        if (!data.success) throw new Error(data.error);
        renderTasks(data.data);
    } catch (err) {
        container.innerHTML = `<p style="color:red;">Failed to load tasks: ${err.message}</p>`;
    }
}

function renderTasks(tasks) {
    const container = document.getElementById('tasksGrid');
    if (!tasks.length) {
        container.innerHTML = "<p>No tasks yet.</p>";
        return;
    }
    container.innerHTML = tasks.map(task => `
        <div class="task-card">
            <h3>${task.title}</h3>
            <p>Status: ${task.status}</p>
            <p>Priority: ${task.priority}</p>
            <p>${task.description || ''}</p>
        </div>
    `).join('');
}

async function createTask(event) {
    event.preventDefault();
    const form = event.target;
    const data = {
        title: form.title.value,
        status: form.status.value,
        priority: form.priority.value,
        assigned_to: form.assigned_to.value,
        due_date: form.due_date.value,
        description: form.description.value,
    };
    try {
        const res = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await res.json();
        if (!result.success) throw new Error(result.error);
        form.reset();
        loadTasks();
    } catch (err) {
        alert("Error creating task: " + err.message);
    }
}
