from fastapi import FastAPI
from app.core.exception_handlers import register_exception_handlers
from app.routes import register_routers
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Wrapity", description="Music-based social network API", version="0.1.0"
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
