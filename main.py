from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="User Management API",
    description="A template demonstrating REST API best practices with FastAPI",
    version="1.0.0",
)

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class User(UserCreate):
    id: int


# --- IN-MEMORY "DATABASE" ---
users_db: List[User] = []


# --- ROUTES ---
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {"message": "API is running"}


@app.get("/users", response_model=List[User], tags=["Users"])
async def list_users(skip: int = 0, limit: int = 10):
    """
    Get a paginated list of users.
    - **skip**: number of items to skip
    - **limit**: maximum number of items to return
    """
    return users_db[skip: skip + limit]


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate):
    """
    Create a new user.
    """
    new_user = User(id=len(users_db) + 1, **user.dict())
    users_db.append(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int):
    """
    Retrieve a user by their ID.
    """
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(user_id: int, updated_user: UserCreate):
    """
    Update an existing user.
    """
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db[index] = User(id=user_id, **updated_user.dict())
            return users_db[index]
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(user_id: int):
    """
    Delete a user by ID.
    """
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
