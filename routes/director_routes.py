from typing import List
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from database.database import get_db
from schema.director_schema import DirectorCreate, DirectorResponse, DirectorUpdate
import controller.director_controller as controller

router = APIRouter(
    prefix="/director",
    tags=["Director"]
)

@router.get(
    "/",
    response_model=List[DirectorResponse],
    summary="All directors",
    description="Seen all directors"
)

def watch_directors(
    skip:int = Query(0, ge=0, description="Number record"),
    limit:int = Query(100, ge=1, le=100, description="Number record"),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)

@router.post(
    "/",
    response_model=DirectorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new director",
    description="Upload a new director"
)

def create_new_director(
    director_data: DirectorCreate,
    db:Session=Depends(get_db)
):
    return controller.create_director(db=db, director_data=director_data)

@router.put(
    "/{director_id}",
    response_model=DirectorResponse,
    summary="Update a director",
    description="Update information of an existing director"
)

def update_existing_director(
    director_data: DirectorUpdate,
    director_id: int = Path(..., ge=1, description="The director's ID to update"),
    db: Session = Depends(get_db)
):
    return controller.update_director(db=db, director_id=director_id, director_data=director_data)

@router.delete(
    "/{director_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a director",
    description="Delete an existing director by ID"
)

def delete_existing_director(
    director_id: int = Path(..., ge=1, description="The director's ID to delete"),
    db: Session = Depends(get_db)
):
    return controller.delete_director(db=db, director_id=director_id)