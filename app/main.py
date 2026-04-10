from fastapi import FastAPI
from app.core.exception_handlers import register_exception_handlers
from app.routes import register_routers
import app.models

app = FastAPI(
    title="Wrapity", description="Music-based social network API", version="0.1.0"
)

register_exception_handlers(app)
register_routers(app)


@app.get("/")
def root():
    return {"message": "Wrapity API is running"}
