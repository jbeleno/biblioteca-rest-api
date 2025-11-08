from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime


def _clean_isbn(isbn: str) -> str:
    if not isbn:
        raise ValueError('ISBN no puede estar vacío')
    cleaned = isbn.replace('-', '').replace(' ', '')
    if not cleaned.isdigit():
        raise ValueError('ISBN debe contener solo dígitos')
    if len(cleaned) not in [10, 13]:
        raise ValueError('ISBN debe tener 10 o 13 dígitos')
    return cleaned


def _validate_year(year: int) -> int:
    if year is None:
        raise ValueError('Año de publicación es requerido')
    current_year = datetime.now().year
    if year <= 1000:
        raise ValueError('Año de publicación debe ser mayor a 1000')
    if year > current_year:
        raise ValueError(f'Año de publicación no puede ser mayor al año actual ({current_year})')
    return year


class AutorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)


class AutorCreate(AutorBase):
    pass


class AutorResponse(AutorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=300)
    isbn: str = Field(...)
    ano_publicacion: int = Field(...)
    autor_id: int = Field(...)
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v):
        return _clean_isbn(v)
    
    @field_validator('ano_publicacion')
    @classmethod
    def validate_ano_publicacion(cls, v):
        return _validate_year(v)


class LibroCreate(LibroBase):
    pass


class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=300)
    isbn: Optional[str] = None
    ano_publicacion: Optional[int] = None
    autor_id: Optional[int] = None
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v):
        if v is None:
            return v
        return _clean_isbn(v)
    
    @field_validator('ano_publicacion')
    @classmethod
    def validate_ano_publicacion(cls, v):
        if v is None:
            return v
        return _validate_year(v)
    
    @model_validator(mode='after')
    def validate_at_least_one_field(self):
        if all(v is None for v in self.model_dump().values()):
            raise ValueError('Al menos un campo debe ser proporcionado para actualizar')
        return self


class LibroResponse(LibroBase):
    id: int
    autor: AutorResponse
    created_at: datetime

    class Config:
        from_attributes = True


class LibroSearchParams(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None


class LibroListParams(BaseModel):
    autor_id: Optional[int] = None
    ano: Optional[int] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)



