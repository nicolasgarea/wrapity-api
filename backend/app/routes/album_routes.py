from fastapi import APIRouter, Depends, HTTPException, Query
from app.clients.albums_client import AlbumsClient
from app.services.album_services import AlbumService
from app.schemas.album_schemas import Album

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


@router.get("/{album_id}", response_model=Album)
async def get_by_id(album_id: int, service: AlbumService = Depends(get_album_service)):
    try:
        return await service.get_details(album_id)
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=str(e))
