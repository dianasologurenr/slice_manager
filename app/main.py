from fastapi import Depends, FastAPI

from routers import users
from routers import availability_zones
from routers import security
from routers import nodes
from routers import ports

from routers import inbound
from routers import slices
from routers import outbound
from routers import flavors
from routers import monitoreo
from routers import images


app = FastAPI()

app.include_router(users.router)
app.include_router(slices.router)
app.include_router(nodes.router)
app.include_router(ports.router)
app.include_router(images.router)
app.include_router(flavors.router)
app.include_router(security.router)
app.include_router(inbound.router)
app.include_router(outbound.router)
app.include_router(availability_zones.router)
app.include_router(monitoreo.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
