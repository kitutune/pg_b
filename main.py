from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool

todos = []

@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    return todos

@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    todos.append(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoItem):
    for index, item in enumerate(todos):
        if item.id == todo_id:
            todos[index] = todo
            return todo
    return None

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    global todos
    todos = [item for item in todos if item.id != todo_id]
    return {"message": "Todo deleted successfully"}
