from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import Response

import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv("DATABASE_URL")

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    
class TaskUpdate(BaseModel):
    title: str
    done: bool
    
def get_db_connection():
    conn=psycopg.connect(DATABASE)
    return conn

def init_db():
    conn=get_db_connection()
    conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks(
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL)
                """)
    count = conn.execute(
        "SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        cur=conn.cursor()
        cur.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [   ("Learn FastAPI", False),
                ("Build CRUD", False),
                ("Submit Assignment", False)
            ]
        )
    conn.commit()
    conn.close()
    
    
@app.get("/", summary="API Information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
    
    
@app.get("/health", summary="Health Check")
def health():
    return {
        "status": "ok"
    }

@app.on_event("startup")
def startup():
    init_db()

@app.get("/tasks", summary="Get All Tasks")
def get_tasks():
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
        for row in rows
        ]


@app.get("/tasks/{task_id}", summary="Get Task By ID")
def get_task(task_id: int):
    conn = get_db_connection()
    
    cur=conn.cursor()
    cur.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }
    
    
@app.post("/tasks", status_code=201, summary="Create Task")
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(
        """
        INSERT INTO tasks (title, done) 
        VALUES (%s, %s)
        RETURNING id,title,done
        """,
        (task.title, False)
    )
    row=cur.fetchone()
    conn.commit()
    conn.close()
    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }

@app.put("/tasks/{task_id}", summary="Update Task")
def update_task(task_id: int, updated: TaskUpdate):
    if updated.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty")
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(
        """
        UPDATE tasks
        SET title = %s, done = %s
        WHERE id = %s
        """,
        (updated.title, updated.done, task_id))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found")
    cur.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,))
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }
    
    
@app.delete("/tasks/{task_id}", status_code=204, summary="Delete Task")
def delete_task(task_id: int):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    conn.commit()
    conn.close()
    return Response(status_code=204)