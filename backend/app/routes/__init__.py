from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.review_routes import router as review_router
from app.routes.favorite_routes import router as favorite_router
from app.routes.follower_routes import router as follower_router
from app.routes.album_routes import router as album_router


def register_routers(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(review_router)
    app.include_router(favorite_router)
    app.include_router(follower_router)
    app.include_router(album_router)
