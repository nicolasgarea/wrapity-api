from app.clients.artists_client import ArtistsClient
from app.schemas.album_schemas import Album, Artist
from app.core.exceptions import ArtistNotFoundException


class ArtistService:
    def __init__(self, client: ArtistsClient):
        self.client = client

    async def search_artists(self, query: str) -> list[Artist]:
        if not query.strip():
            return []

        raw_data = await self.client.get_artists_by_name(query)
        if not raw_data or "error" in raw_data:
            raise ArtistNotFoundException("No artists found")

        return [Artist.model_validate(item) for item in raw_data.get("data", [])]

    async def get_details(self, artist_id: int) -> Artist:
        raw_data = await self.client.get_artist_by_id(artist_id)
        if not raw_data or "error" in raw_data:
            raise ArtistNotFoundException(f"Artist {artist_id} not found")

        return Artist.model_validate(raw_data)

    async def get_albums(self, artist_id: int) -> list[Album]:
        artist = await self.get_details(artist_id)

        raw_data = await self.client.get_artist_albums(artist_id)
        if not raw_data or "error" in raw_data:
            raise ArtistNotFoundException(f"Artist {artist_id} not found")

        items = raw_data.get("data", [])
        items.sort(key=lambda item: item.get("release_date") or "", reverse=True)

        artist_ref = {"id": artist.id, "name": artist.name, "picture": artist.picture}
        for item in items:
            item["artist"] = artist_ref

        return [Album.model_validate(item) for item in items]
