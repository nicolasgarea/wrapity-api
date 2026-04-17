from pydantic import BaseModel, model_validator


class Artist(BaseModel):
    id: int
    name: str


class Album(BaseModel):
    id: int
    title: str
    cover: str | None = None
    artist: Artist

    @model_validator(mode="before")
    def pick_best_cover(cls, values):
        values["cover"] = (
            values.get("cover_xl")
            or values.get("cover_big")
            or values.get("cover_medium")
            or values.get("cover")
        )
        return values


class AlbumWithReview(BaseModel):
    id: int
    album: Album
    rating: float | None = None
    review: str | None = None


class AlbumSearchResponse(BaseModel):
    data: list[Album]


class AlbumTrendingResponse(BaseModel):
    data: list[Album]
