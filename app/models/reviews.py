from database import Base
from sqlalchemy import Column, Integer, String

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario = Column(String)
    review = Column(String)
    serie_filme = Column(Integer)
    estrelas = Column(Integer)

    def __repr__(self):
        return f"<Review {self.id} {self.usuario} {self.review} {self.serie_filme} {self.estrelas}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "review": self.review,
            "serie_filme": self.serie_filme,
            "estrelas": self.estrelas
        }
