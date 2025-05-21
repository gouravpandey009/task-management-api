
---

````markdown
# 💼 Softblend Task Management API

> **Elegant. Secure. Scalable.**  
> A complete RESTful Task Management backend — built with real-world standards in mind.

---

## 🧠 Why This Stands Out

This isn’t just a CRUD app — it’s a **production-grade backend skeleton** that:
- Follows **RESTful best practices**
- Implements **API key authentication**
- Offers **robust error handling** and **input validation**
- Supports **pagination, filtering**, and **Dockerized deployment**
- Uses **PostgreSQL**, **Flask**, and **modular architecture** for scalability

---

## 🧩 Problem Statement (from Softblend)

> Build a simple RESTful API for a Task Management App (like Trello or Todoist) with user and task management functionality.

---

## 🛠 Tech Stack

| Layer            | Tech                        |
|------------------|-----------------------------|
| Language         | Python 3.10                 |
| Framework        | Flask                       |
| ORM              | SQLAlchemy                  |
| Database         | PostgreSQL                  |
| Auth             | API Key (via HTTP header)   |
| DevOps           | Docker + Docker Compose     |
| Config           | python-dotenv (.env based)  |

---

## 🧱 Folder Structure

```bash
task_management_api/
│
├── app/
│   ├── __init__.py              # App initialization
│   ├── models.py                # SQLAlchemy models
│   ├── routes/
│   │   ├── user_routes.py       # User endpoints
│   │   └── task_routes.py       # Task endpoints
│   └── utils/
│       └── auth.py              # API Key auth
│
├── config.py                    # DB and config loader
├── run.py                       # App entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env                         # Local secrets
└── README.md
````

---

## 🚀 Features Overview

✅ **User APIs**

* Create users
* Fetch user by ID
* List all users

✅ **Task APIs**

* Full CRUD on tasks
* Query by `status`, `assignedUserId`
* Pagination support

✅ **Security**

* API key-based auth via `x-api-key` header

✅ **Production Readiness**

* Dockerized
* Uses `.env` for sensitive configs
* Follows modular Flask design

✅ **Error Handling**

* Clear JSON errors with proper status codes (400/401/404/409)

---

## 📦 Setup Guide

### 🔧 1. Clone the Repo

```bash
git clone https://github.com/gouravpandey009/task-management-api.git
cd task-management-api
```

### 🛠️ 2. Create `.env`

```env
DATABASE_URL=postgresql://postgres:1234@localhost:5432/task_management
API_KEY=softblend123
```

### 🗃️ 3. Start PostgreSQL Locally (if not using Docker)

Make sure PostgreSQL is running with:

* DB: `task_management`
* User: `postgres`
* Password: `1234`

### 🧪 4. Run Without Docker

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

### 🐳 5. Or Run With Docker

```bash
docker-compose build
docker-compose up
```

---

## 🔐 Authentication

All endpoints require an `x-api-key` header with the correct API Key:

```http
x-api-key: softblend123
```

🔒 Unauthorized requests return `401 Unauthorized`.

---

## 📘 API Reference — Documentation

---

### 👤 USER ENDPOINTS

---

#### 📌 `POST /users` — Create a New User

Creates a new user in the system.

**Headers:**

```
Content-Type: application/json
x-api-key: softblend123
```

**Request Body:**

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Success Response:**

```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Status Codes:**

* `201 Created` – User successfully created
* `409 Conflict` – Email already exists
* `400 Bad Request` – Missing required fields

---

#### 📌 `GET /users/:id` — Get User by ID

**Example:** `/users/1`

**Success Response:**

```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Status Codes:**

* `200 OK`
* `404 Not Found` – User does not exist

---

#### 📌 `GET /users` — Get All Users

Returns a list of all users in the system.

**Success Response:**

```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "John",
    "email": "john@example.com"
  }
]
```

**Status Code:** `200 OK`

---

### ✅ TASK ENDPOINTS

---

#### 📌 `POST /tasks` — Create Task

**Headers:**

```
Content-Type: application/json
x-api-key: softblend123
```

**Request Body:**

```json
{
  "title": "Complete README",
  "description": "Polish the API reference",
  "due_date": "2025-05-28",
  "status": "pending",
  "assignedUserId": 1
}
```

**Success Response:**

```json
{
  "id": 5,
  "title": "Complete README",
  "description": "Polish the API reference",
  "due_date": "2025-05-28",
  "status": "pending",
  "assignedUserId": 1
}
```

**Status Codes:**

* `201 Created`
* `400 Bad Request` – Invalid/missing fields
* `404 Not Found` – Assigned user does not exist

---

#### 📌 `GET /tasks/:id` — Get Task by ID

**Example:** `/tasks/1`

**Success Response:**

```json
{
  "id": 1,
  "title": "Initial Setup",
  "description": "Create project skeleton",
  "due_date": "2025-05-20",
  "status": "done",
  "assignedUserId": 2
}
```

**Status Codes:**

* `200 OK`
* `404 Not Found`

---

#### 📌 `GET /tasks` — Get All Tasks (with Filters + Pagination)

**Query Parameters:**

| Param            | Type    | Description                                      |
| ---------------- | ------- | ------------------------------------------------ |
| `status`         | string  | Filter tasks by `pending`, `in_progress`, `done` |
| `assignedUserId` | integer | Filter tasks assigned to a specific user         |
| `page`           | integer | Page number (for pagination)                     |
| `limit`          | integer | Results per page                                 |

**Example:**

```http
GET /tasks?status=done&assignedUserId=2&page=1&limit=5
```

**Success Response:**

```json
{
  "page": 1,
  "limit": 5,
  "total": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Setup PostgreSQL",
      "status": "done"
    },
    {
      "id": 2,
      "title": "Dockerize project",
      "status": "done"
    }
  ]
}
```

**Status Code:** `200 OK`

---

#### 📌 `PUT /tasks/:id` — Update Task

**Example:** `/tasks/1`

**Request Body (any field can be updated):**

```json
{
  "title": "Updated Title",
  "status": "in_progress",
  "due_date": "2025-05-30"
}
```

**Success Response:**

```json
{
  "id": 1,
  "title": "Updated Title",
  "status": "in_progress",
  "due_date": "2025-05-30",
  "assignedUserId": 1
}
```

**Status Codes:**

* `200 OK`
* `400 Bad Request`
* `404 Not Found`

---

#### 📌 `DELETE /tasks/:id` — Delete Task

**Example:** `/tasks/3`

**Success Response:**

```json
{
  "message": "Task deleted successfully"
}
```

**Status Codes:**

* `200 OK`
* `404 Not Found`

---

## 🔁 Postman Collection (Live Docs)

📘 Explore the complete API live on Postman:  
👉 [Softblend Task Management API Docs](https://documenter.getpostman.com/view/31280959/2sB2qZF3Lm)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/31280959/2sB2qZF3Lm)

---

## 🧪 Example Error Responses

| Code | Meaning               | Example Message                  |
| ---- | --------------------- | -------------------------------- |
| 400  | Bad Request           | `Missing field: "email"`         |
| 401  | Unauthorized          | `Invalid or missing API key`     |
| 404  | Not Found             | `Task/User not found`            |
| 409  | Conflict              | `User with email already exists` |
| 500  | Internal Server Error | `Unexpected error occurred`      |

---








