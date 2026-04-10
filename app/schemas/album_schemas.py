from pydantic import BaseModel


class Artist(BaseModel):
    id: int
    name: str


class Album(BaseModel):
    id: int
    title: str
    cover: str
    artist: Artist


class AlbumWithReview(BaseModel):
    id: int
    album: Album
    rating: float | None = None
    review: str | None = None


class AlbumSearchResponse(BaseModel):
    data: list[Album]


class AlbumTrendingResponse(BaseModel):
    data: list[Album]
