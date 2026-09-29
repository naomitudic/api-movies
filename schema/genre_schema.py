from typing import List, Optional
from pydantic import BaseModel, Field

from schema.simple_schema import (
    GenreBase,
    GenreResponse,
    MovieSimpleResponse,
)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length=1, max_length=100)


class GenreDetailResponse(GenreResponse):

    movies: List[MovieSimpleResponse] = Field(
        default=[],
        description="List movies"
    )
