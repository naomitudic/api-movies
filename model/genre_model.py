from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.database import Base

movie_genres = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movie.id", ondelete="CASCADE"), primary_key=True),
    Column("genres_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)

class Genre(Base):

    __tablename__= "genres"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)

    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

    def __repr__(self)->str:
        return f"<Genre(id={self.id}, name='{self.name}')>"