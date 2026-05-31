from app.core.config import DEEZER_BASE_URL
import httpx


class AlbumsClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=DEEZER_BASE_URL)

    async def get_album_trends(self):
        try:
            response = await self.client.get(
                "/search/album", params={"q": "album", "order": "RANKING", "limit": 20}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Error fetching albums: {e.response.status_code}"
            ) from e

    async def get_albums_by_name(self, q: str):
        try:
            response = await self.client.get("/search/album", params={"q": q})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Error fetching albums: {e.response.status_code}"
            ) from e

    async def get_album_by_id(self, album_id: int):
        try:
            response = await self.client.get(f"/album/{album_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Error fetching album: {e.response.status_code}") from e

    async def close(self):
        await self.client.aclose()
