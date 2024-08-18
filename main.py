
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoItem(BaseModel):
    id: Optional[int] = Field(None, description="The unique identifier for a todo item.")
    title: str
    completed: bool


todos: List[TodoItem] = []


@app.get("/todos", response_model=List[TodoItem])
async def get_todos() -> List[TodoItem]:
    """Get all todo items."""
    return todos


@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem) -> TodoItem:
    """Create a new todo item."""
    # id をバックエンドで生成
    todo.id = todos[-1].id + 1 if todos else 1
    todos.append(todo)
    return todo


@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoItem) -> TodoItem:
    """Update an existing todo item."""
    for index, item in enumerate(todos):
        if item.id == todo_id:
            todos[index] = todo
            return todo
    raise HTTPException(status_code=404, detail="Todo item not found")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int) -> dict:
    """Delete a todo item."""
    global todos
    todos = [item for item in todos if item.id != todo_id]
    return {"message": "Todo deleted successfully"}
