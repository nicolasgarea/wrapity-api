from app.core.config import DEEZER_BASE_URL
from cachetools import TTLCache
import httpx


class AlbumsClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=DEEZER_BASE_URL)
        self._album_cache: TTLCache = TTLCache(maxsize=2000, ttl=86400)
        self._trends_cache: TTLCache = TTLCache(maxsize=1, ttl=1800)

    async def get_album_trends(self):
        if "trends" in self._trends_cache:
            return self._trends_cache["trends"]
        try:
            response = await self.client.get(
                "/search/album", params={"q": "album", "order": "RANKING", "limit": 20}
            )
            response.raise_for_status()
            data = response.json()
            self._trends_cache["trends"] = data
            return data
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
        if album_id in self._album_cache:
            return self._album_cache[album_id]
        try:
            response = await self.client.get(f"/album/{album_id}")
            response.raise_for_status()
            data = response.json()
            self._album_cache[album_id] = data
            return data
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Error fetching album: {e.response.status_code}") from e

    async def close(self):
        await self.client.aclose()
