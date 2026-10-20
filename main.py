from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Разрешаем запросы с нашего сайта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем базу данных (создастся автоматически)
conn = sqlite3.connect('pms.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        customer TEXT,
        status TEXT
    )
''')
conn.commit()

# Модель данных для создания проекта
class Project(BaseModel):
    name: str
    customer: str
    status: str

# Эндпоинт для получения списка проектов
@app.get("/api/projects")
def get_projects():
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    projects = []
    for row in rows:
        projects.append({"id": row[0], "name": row[1], "customer": row[2], "status": row[3]})
    return projects

# Эндпоинт для создания проекта
@app.post("/api/projects")
def create_project(project: Project):
    cursor.execute("INSERT INTO projects (name, customer, status) VALUES (?, ?, ?)",
                   (project.name, project.customer, project.status))
    conn.commit()
    return {"message": "Проект успешно создан"}
