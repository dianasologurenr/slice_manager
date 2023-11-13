from fastapi import Depends, FastAPI

from routers import users

from routers import slices

app = FastAPI()

app.include_router(users.router)

app.include_router(slices.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
