from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.clients.albums_client import AlbumsClient
from app.core.exception_handlers import register_exception_handlers
from app.routes import register_routers
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.albums_client = AlbumsClient()
    yield
    await app.state.albums_client.close()


app = FastAPI(
    title="Wrapity",
    description="Music-based social network API",
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
register_routers(app)


@app.get("/")
def root():
    return {"message": "Wrapity API is running"}
