from fastapi import APIRouter, Depends, Query
from app.clients.albums_client import AlbumsClient
from app.routes.favorite_routes import get_favorite_repository
from app.repositories.favorite_repositories import FavoriteRepository
from app.services.album_services import AlbumService
from app.schemas.album_schemas import Album, AlbumDetail

router = APIRouter(prefix="/albums", tags=["albums"])


async def get_album_service():
    client = AlbumsClient()
    try:
        yield AlbumService(client)
    finally:
        await client.close()


@router.get("/trending", response_model=list[Album])
async def get_trending(service: AlbumService = Depends(get_album_service)):
    return await service.get_trending_albums()


@router.get("/search", response_model=list[Album])
async def search(
    q: str = Query(..., min_length=1),
    service: AlbumService = Depends(get_album_service),
):
    return await service.search_albums(q)


@router.get("/{album_id}", response_model=AlbumDetail)
async def get_by_id(
    album_id: int,
    service: AlbumService = Depends(get_album_service),
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository),
):
    album = await service.get_details(album_id)
    album.favorite_count = favorite_repo.count_by_album_id(album_id)
    return album
