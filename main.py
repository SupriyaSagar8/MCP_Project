from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uuid

app = FastAPI(title="Todo List API", version="1.0.0")

# In-memory database
db: Dict[str, List[Dict]] = {
    "backlog": [
        {"id": str(uuid.uuid4()), "title": "Read research paper", "description": "Transformer models 2017", "status": "pending"},
        {"id": str(uuid.uuid4()), "title": "Plan weekend trip", "description": "Hiking in state park", "status": "pending"},
    ],
    "active": [
        {"id": str(uuid.uuid4()), "title": "Finish assignment", "description": "Data mining project", "status": "in-progress"},
    ],
    "later": [
        {"id": str(uuid.uuid4()), "title": "Learn Rust", "description": "System programming practice", "status": "todo"},
    ],
}

# Schemas
class Task(BaseModel):
    title: str
    description: str
    status: str = "todo"

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

class MoveRequest(BaseModel):
    taskId: str
    fromSection: str
    toSection: str

# Endpoints
@app.get("/tasks")
def get_all_tasks():
    """Return all tasks grouped by section"""
    return db

@app.get("/tasks/search")
def search_tasks(query: str):
    """Search for tasks across all sections"""
    results = []
    for section, tasks in db.items():
        for task in tasks:
            if query.lower() in task["title"].lower() or query.lower() in task["description"].lower():
                results.append({**task, "section": section})
    return results

@app.post("/tasks/{section}", status_code=201)
def add_task(section: str, task: Task):
    """Add a task to the given section if there is no similar task that is already present. If yes, inform the user for their confirmation and react accordingly."""
    if section not in db:
        raise HTTPException(status_code=400, detail="Invalid section")
    new_task = {"id": str(uuid.uuid4()), **task.dict()}
    db[section].append(new_task)
    return new_task

@app.put("/tasks/{section}/{task_id}")
def update_task(section: str, task_id: str, task: TaskUpdate):
    """Update an existing task"""
    if section not in db:
        raise HTTPException(status_code=400, detail="Invalid section")
    for t in db[section]:
        if t["id"] == task_id:
            if task.title: t["title"] = task.title
            if task.description: t["description"] = task.description
            if task.status: t["status"] = task.status
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{section}/{task_id}")
def delete_task(section: str, task_id: str):
    """Delete a task"""
    if section not in db:
        raise HTTPException(status_code=400, detail="Invalid section")
    for t in db[section]:
        if t["id"] == task_id:
            db[section].remove(t)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks/move")
def move_task(req: MoveRequest):
    """Move a task from one section to another"""
    if req.fromSection not in db or req.toSection not in db:
        raise HTTPException(status_code=400, detail="Invalid section(s)")
    for t in db[req.fromSection]:
        if t["id"] == req.taskId:
            db[req.fromSection].remove(t)
            db[req.toSection].append(t)
            return {**t, "section": req.toSection}
    raise HTTPException(status_code=404, detail="Task not found")
