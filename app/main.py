from fastapi import Depends, FastAPI

from routers import users
from routers import availability_zones
from routers import security

app = FastAPI()

app.include_router(users.router)
app.include_router(availability_zones.router)
app.include_router(security.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
