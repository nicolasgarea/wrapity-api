from fastapi import APIRouter, Depends, Query
from app.clients.artists_client import ArtistsClient
from app.services.artist_services import ArtistService
from app.schemas.album_schemas import Album, Artist

router = APIRouter(prefix="/artists", tags=["artists"])


async def get_artist_service():
    client = ArtistsClient()
    try:
        yield ArtistService(client)
    finally:
        await client.close()


@router.get("/search", response_model=list[Artist])
async def search(
    q: str = Query(..., min_length=1),
    service: ArtistService = Depends(get_artist_service),
):
    return await service.search_artists(q)


@router.get("/{artist_id}", response_model=Artist)
async def get_by_id(
    artist_id: int,
    service: ArtistService = Depends(get_artist_service),
):
    return await service.get_details(artist_id)


@router.get("/{artist_id}/albums", response_model=list[Album])
async def get_albums(
    artist_id: int,
    service: ArtistService = Depends(get_artist_service),
):
    return await service.get_albums(artist_id)
