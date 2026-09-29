from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from schema.director_schema import DirectorResponse
from schema.simple_schema import (
    MovieBase,
    MovieSimpleResponse,
    GenreResponse,
)


class MovieCreate(MovieBase):

    genre_ids: Optional[List[int]] = Field(
        default=[],
        description="Genre's ID list",
        examples=[[1, 2]]
    )


class MovieUpdate(BaseModel):

    title: Optional[str] = Field(None, min_length=1, max_length=150)
    director_id: Optional[int] = None
    genre_ids: Optional[List[int]] = Field(None, description="Update genre's ID list")
    duration: Optional[int] = Field(None, gt=0)
    year: Optional[int] = Field(None, ge=1, le=2100)
    is_available: Optional[bool] = Field(None)


class MovieResponse(MovieSimpleResponse):

    director: Optional[DirectorResponse] = None
    genres: List[GenreResponse] = []

    model_config = ConfigDict(from_attributes=True)
