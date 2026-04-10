from app.clients.albums_client import AlbumsClient
from app.schemas.album_schemas import Album, AlbumSearchResponse
from app.core.exceptions import AlbumNotFoundException


class AlbumService:
    def __init__(self, client: AlbumsClient):
        self.client = client

    async def get_trending_albums(self) -> list[Album]:
        raw_data = await self.client.get_album_trends()
        if not raw_data or "error" in raw_data:
            raise AlbumNotFoundException("No trending albums found")

        validated = AlbumSearchResponse.model_validate(raw_data)
        return validated.data

    async def search_albums(self, query: str) -> list[Album]:
        if not query.strip():
            return []

        raw_data = await self.client.get_albums_by_name(query)
        if not raw_data or "error" in raw_data:
            raise AlbumNotFoundException("No albums found")

        validated = AlbumSearchResponse.model_validate(raw_data)
        return validated.data

    async def get_details(self, album_id: int) -> Album:
        raw_data = await self.client.get_album_by_id(album_id)
        if not raw_data or "error" in raw_data:
            raise AlbumNotFoundException(f"Album {album_id} not found")

        return Album.model_validate(raw_data)
