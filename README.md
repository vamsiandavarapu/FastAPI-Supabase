# FastAPI-Docker-CRUDAPP

A Task CRUD API built with **FastAPI**, **PostgreSQL**, and **Docker Compose**.

This project demonstrates migrating a FastAPI CRUD application from SQLite to PostgreSQL and running the complete application stack using Docker.

## Tech Stack

* Python 3.13
* FastAPI
* Uvicorn
* PostgreSQL 18
* Psycopg
* Docker
* Docker Compose

## Architecture

```text
Client
  │
  ▼
FastAPI API Container
  │
  │ db:5432
  ▼
PostgreSQL Container
  │
  ▼
Docker Volume
taskdata
```

The API and database are started together using Docker Compose.

## Run the Application

Clone the repository and create a `.env` file using `.env.example` as a template.

Then run:

```bash
docker compose up
```

The API will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

## Environment Variables

The application uses `DATABASE_URL` for the database connection.

Example:

```text
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

The real `.env` file is excluded from Git using `.gitignore`.

`.env.example` is included as a template.

## API Endpoints

| Method | Endpoint      | Description      | Success |
| ------ | ------------- | ---------------- | ------- |
| GET    | `/tasks`      | Get all tasks    | 200     |
| GET    | `/tasks/{id}` | Get a task by ID | 200     |
| POST   | `/tasks`      | Create a task    | 201     |
| PUT    | `/tasks/{id}` | Update a task    | 200     |
| DELETE | `/tasks/{id}` | Delete a task    | 204     |

Unknown task IDs return `404`.

Invalid/empty task titles return `400`.

## Example Request

```bash
curl -i http://localhost:8000/tasks
```

Example response:

```text
HTTP/1.1 200 OK
```

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  },
  {
    "id": 2,
    "title": "Build CRUD",
    "done": false
  },
  {
    "id": 3,
    "title": "Submit Assignment",
    "done": false
  }
]
```

## PostgreSQL

PostgreSQL runs inside a Docker container.

The database is:

```text
Database: tasks
User: postgres
Port: 5432
```

The PostgreSQL data is stored in the Docker volume:

```text
taskdata
```

This provides persistence across container restarts.

## Persistence Test

The database persistence was verified by:

```bash
docker compose down
docker compose up
```

Tasks created before the restart remained available after the containers were recreated.

## Database Verification

PostgreSQL can be accessed using:

```bash
docker compose exec db psql -U postgres -d tasks
```

Then:

```sql
SELECT * FROM tasks;
```

Database screenshot:

> Add the PostgreSQL `SELECT * FROM tasks;` screenshot here before final submission.

## Project Structure

```text
Docker fastapi/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Key Concepts Demonstrated

* FastAPI CRUD API
* PostgreSQL database
* Parameterized SQL queries
* Environment variables
* Docker images and containers
* Docker volumes
* Docker Compose
* Persistent database storage
* API-to-database communication
