# 🚀 Task Manager API

A full-stack task management web application built using **Flask**, **MongoDB**, and **vanilla HTML/CSS/JavaScript**. Features RESTful APIs, task statistics, filters, and a responsive UI.

---

## 📁 Project Structure
```
task-manager-app/
│
├── app/
│ ├── init.py # Flask app factory
│ ├── routes/
│ │ ├── task_routes.py # /api/tasks endpoints
│ │ └── stats_routes.py # /api/stats endpoint
│ ├── utils/
│ │ ├── db.py # MongoDB connection
│ │ ├── helpers.py # Serializers & ID validator
│ │ └── init.py
│ └── templates/
│ └── index.html # Frontend UI
│
├── static/
│ ├── style.css # Frontend CSS
│ └── script.js # Frontend JS
│
├── run.py # Entry point
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```
---

## ⚙️ Features

- ✅ Create, Read, Update, Delete (CRUD) tasks
- ✅ Filter tasks by status and priority
- ✅ Task statistics dashboard
- ✅ Responsive UI (HTML + CSS)
- ✅ MongoDB for persistent storage
- ✅ RESTful API (JSON format)
- ✅ Modular Flask structure

---

## 🧪 API Endpoints

| Method   | Endpoint               | Description             |
|----------|------------------------|-------------------------|
| `GET`    | `/api/tasks`           | Get all tasks           |
| `GET`    | `/api/tasks?status=x`  | Filter tasks by status  |
| `POST`   | `/api/tasks`           | Create a new task       |
| `GET`    | `/api/tasks/<id>`      | Get a single task       |
| `PUT`    | `/api/tasks/<id>`      | Update a task           |
| `DELETE` | `/api/tasks/<id>`      | Delete a task           |
| `GET`    | `/api/stats`           | Get task stats summary  |

---

## 🧰 Tech Stack

- **Backend**: Python, Flask, PyMongo
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MongoDB
- **Tools**: Postman, Git, VS Code / PyCharm

---

## 🚀 Getting Started

### 1️⃣ Clone the repo

```bash
git clone https://github.com/yourusername/task-manager-app.git
cd task-manager-app
