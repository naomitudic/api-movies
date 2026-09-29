
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database.database import get_db
from schema.movie_schema import MovieCreate, MovieResponse
import controller.movie_controller as controller

router = APIRouter(
    prefix="/movie",
    tags=["Movie"]
)

@router.get(
    "/",
    response_model=List[MovieResponse],
    summary="All movies",
    description="Seen all movies"
)

def watch_movies(
    skip:int = Query(0, ge=0, description="Number record"),
    limit:int = Query(100, ge=1, le=100, description="Number record"),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)

@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new movie",
    description="Upload a new movie"
)

def create_new_movie(
    movie_data: MovieCreate,
    db:Session=Depends(get_db)
):
    return controller.create_movie(db=db, movie_data=movie_data)