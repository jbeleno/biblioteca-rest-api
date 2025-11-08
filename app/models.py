from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    libros = relationship("Libro", back_populates="autor", cascade="all, delete-orphan")


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(300), nullable=False, index=True)
    isbn = Column(String(17), nullable=False, unique=True, index=True)
    ano_publicacion = Column(Integer, nullable=False, index=True)
    autor_id = Column(Integer, ForeignKey("autores.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    autor = relationship("Autor", back_populates="libros")

    __table_args__ = (
        CheckConstraint('ano_publicacion > 1000', name='check_ano_valido'),
    )

