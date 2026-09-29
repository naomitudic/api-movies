from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Movie title",
        examples=["Titanic"]
    )

    director_id: Optional[int] = Field(
        default=None,
        description="Director's ID"
    )

    duration: int = Field(
        ...,
        gt=0,
        description="Movie duration",
        examples=[194]
    )

    year: int = Field(
        ...,
        ge=1888,
        le=2100,
        description="Movie year",
        examples=[1997]
    )

    is_available: bool = Field(
        default=True,
        description="This movie is available",
        examples=[True]
    )


class MovieSimpleResponse(MovieBase):

    id: int = Field(..., description="PK database", examples=[1])
    model_config = ConfigDict(from_attributes=True)


class GenreBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=100, examples=["Sci-Fi"])


class GenreResponse(GenreBase):

    id: int = Field(..., description="Primary key")
    model_config = ConfigDict(from_attributes=True)
