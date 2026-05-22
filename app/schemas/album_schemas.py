from pydantic import BaseModel, model_validator


class Artist(BaseModel):
    id: int
    name: str
    picture: str | None = None
    nb_album: int | None = None

    @model_validator(mode="before")
    def pick_best_picture(cls, values):
        if isinstance(values, dict):
            values["picture"] = (
                values.get("picture_xl")
                or values.get("picture_big")
                or values.get("picture_medium")
                or values.get("picture")
            )
        return values


class Album(BaseModel):
    id: int
    title: str
    cover: str | None = None
    artist: Artist

    @model_validator(mode="before")
    def pick_best_cover(cls, values):
        if isinstance(values, dict):
            values["cover"] = (
                values.get("cover_xl")
                or values.get("cover_big")
                or values.get("cover_medium")
                or values.get("cover")
            )
        return values


class Genre(BaseModel):
    id: int
    name: str
    picture: str | None = None


class Track(BaseModel):
    id: int
    title: str
    duration: int
    track_position: int | None = None
    disk_number: int | None = None
    preview: str | None = None
    explicit_lyrics: bool | None = None


class AlbumDetail(Album):
    favorite_count: int = 0
    release_date: str | None = None
    nb_tracks: int | None = None
    duration: int | None = None
    label: str | None = None
    record_type: str | None = None
    explicit_lyrics: bool | None = None
    genres: list[Genre] = []
    tracks: list[Track] = []

    @model_validator(mode="before")
    def flatten_nested(cls, values):
        if not isinstance(values, dict):
            return values
        genres = values.get("genres")
        if isinstance(genres, dict):
            values["genres"] = genres.get("data", [])
        tracks = values.get("tracks")
        if isinstance(tracks, dict):
            values["tracks"] = tracks.get("data", [])
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
