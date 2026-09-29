from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    biography = Column(String(500), nullable=True)

    movies = relationship("Movie", back_populates="director", cascade="all, delete-orphan")

    def __repr__(self)->str:
        return f"<Director(id={self.id}, name='{self.name}')"