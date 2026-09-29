from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from model.genre_model import movie_genres

class Movie(Base):

    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False, index=True)
    duration = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    director_id = Column(Integer, ForeignKey("directors.id", ondelete="SET NULL"), nullable=True)
    director = relationship("Director", back_populates="movies")

    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")

    def __repr__(self)-> str:
        return f"<Movie(id={self.id}, title={self.title}, director={self.director})"