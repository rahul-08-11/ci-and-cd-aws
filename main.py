from fastapi import FastAPI, Depends
from models import UserItem

app = FastAPI()




@app.get("/")
async def get_home():
    return {"message": "Hello World"}


async def get_username(username : str) -> UserItem:
    return UserItem(username=username)

@app.get("/user")
async def get_user_new(query = Depends(get_username)):
    
    return {
        "username": query.username
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
