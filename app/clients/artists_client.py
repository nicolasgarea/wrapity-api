from app.core.config import DEEZER_BASE_URL
import httpx

ARTIST_ALBUMS_LIMIT = 200


class ArtistsClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=DEEZER_BASE_URL)

    async def get_artist_by_id(self, artist_id: int):
        try:
            response = await self.client.get(f"/artist/{artist_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Error fetching artist: {e.response.status_code}"
            ) from e

    async def get_artists_by_name(self, q: str):
        try:
            response = await self.client.get("/search/artist", params={"q": q})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Error fetching artists: {e.response.status_code}"
            ) from e

    async def get_artist_albums(self, artist_id: int):
        try:
            response = await self.client.get(
                f"/artist/{artist_id}/albums",
                params={"limit": ARTIST_ALBUMS_LIMIT},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Error fetching artist albums: {e.response.status_code}"
            ) from e

    async def close(self):
        await self.client.aclose()
