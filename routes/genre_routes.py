from typing import List
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from database.database import get_db
from schema.genre_schema import GenreCreate, GenreResponse, GenreDetailResponse, GenreUpdate
import controller.genre_controller as controller

router = APIRouter(
    prefix="/genre",
    tags=["Genre"]
)

@router.get(
    "/",
    response_model=List[GenreDetailResponse],
    summary="All genres",
    description="Retrieve a list of all genres"
)
def watch_genres(
    skip:int = Query(0, ge=0, description="Number record"),
    limit:int = Query(100, ge=1, le=100, description="Number record"),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)

@router.get(
    "/{genre_id}",
    response_model=GenreResponse,
    summary="Get genre by ID",
    description="Fetch a specific genre by its ID"
)
def watch_genre(
    genre_id: int = Path(..., ge=1, description="The genre's ID"),
    db: Session = Depends(get_db)
):
    return controller.get_by_id(db=db, genre_id=genre_id)

@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new genre",
    description="Upload a new genre"
)
def create_new_genre(
    genre_data: GenreCreate,
    db:Session=Depends(get_db)
):
    return controller.create_genre(db=db, genre_data=genre_data)

@router.put(
    "/{genre_id}",
    response_model=GenreResponse,
    summary="Update a genre",
    description="Update information of an existing genre"
)
def update_existing_genre(
    genre_data: GenreUpdate,
    genre_id: int = Path(..., ge=1, description="The genre's ID to update"),
    db: Session = Depends(get_db)
):
    return controller.update_genre(db=db, genre_id=genre_id, genre_data=genre_data)

@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a genre",
    description="Delete an existing genre by ID"
)
def delete_existing_genre(
    genre_id: int = Path(..., ge=1, description="The genre's ID to delete"),
    db: Session = Depends(get_db)
):
    return controller.delete_genre(db=db, genre_id=genre_id)