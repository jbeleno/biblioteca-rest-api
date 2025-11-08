from typing import List, Optional
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session, joinedload
from app import models, schemas


def _build_search_query(db: Session, titulo: Optional[str] = None, autor: Optional[str] = None):
    query = db.query(models.Libro)
    conditions = []
    
    if titulo:
        conditions.append(models.Libro.titulo.ilike(f"%{titulo}%"))
    
    if autor:
        conditions.append(models.Autor.nombre.ilike(f"%{autor}%"))
        query = query.join(models.Autor)
    
    if conditions:
        query = query.filter(or_(*conditions))
    
    return query


def get_autor(db: Session, autor_id: int) -> Optional[models.Autor]:
    return db.query(models.Autor).filter(models.Autor.id == autor_id).first()


def get_autor_by_nombre(db: Session, nombre: str) -> Optional[models.Autor]:
    return db.query(models.Autor).filter(models.Autor.nombre == nombre).first()


def create_autor(db: Session, autor: schemas.AutorCreate) -> models.Autor:
    db_autor = models.Autor(nombre=autor.nombre)
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor


def get_libro(db: Session, libro_id: int) -> Optional[models.Libro]:
    return (
        db.query(models.Libro)
        .options(joinedload(models.Libro.autor))
        .filter(models.Libro.id == libro_id)
        .first()
    )


def get_libro_by_isbn(db: Session, isbn: str) -> Optional[models.Libro]:
    return db.query(models.Libro).filter(models.Libro.isbn == isbn).first()


def get_libros(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    autor_id: Optional[int] = None,
    ano: Optional[int] = None
) -> List[models.Libro]:
    query = db.query(models.Libro).options(joinedload(models.Libro.autor))
    
    if autor_id is not None:
        query = query.filter(models.Libro.autor_id == autor_id)
    
    if ano is not None:
        query = query.filter(models.Libro.ano_publicacion == ano)
    
    return query.offset(skip).limit(limit).all()


def count_libros(
    db: Session,
    autor_id: Optional[int] = None,
    ano: Optional[int] = None
) -> int:
    query = db.query(models.Libro)
    
    if autor_id is not None:
        query = query.filter(models.Libro.autor_id == autor_id)
    
    if ano is not None:
        query = query.filter(models.Libro.ano_publicacion == ano)
    
    return query.count()


def search_libros(
    db: Session,
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> List[models.Libro]:
    query = _build_search_query(db, titulo, autor)
    query = query.options(joinedload(models.Libro.autor))
    return query.offset(skip).limit(limit).all()


def count_search_libros(
    db: Session,
    titulo: Optional[str] = None,
    autor: Optional[str] = None
) -> int:
    query = _build_search_query(db, titulo, autor)
    return query.count()


def create_libro(db: Session, libro: schemas.LibroCreate) -> models.Libro:
    autor = get_autor(db, libro.autor_id)
    if not autor:
        raise ValueError(f"Autor con ID {libro.autor_id} no existe")
    
    isbn_clean = libro.isbn.replace('-', '').replace(' ', '')
    existing = get_libro_by_isbn(db, isbn_clean)
    if existing:
        raise ValueError(f"Libro con ISBN {isbn_clean} ya existe")
    
    db_libro = models.Libro(
        titulo=libro.titulo,
        isbn=isbn_clean,
        ano_publicacion=libro.ano_publicacion,
        autor_id=libro.autor_id
    )
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    
    return (
        db.query(models.Libro)
        .options(joinedload(models.Libro.autor))
        .filter(models.Libro.id == db_libro.id)
        .first()
    )


def update_libro(
    db: Session,
    libro_id: int,
    libro_update: schemas.LibroUpdate
) -> Optional[models.Libro]:
    db_libro = get_libro(db, libro_id)
    if not db_libro:
        return None
    
    update_data = libro_update.model_dump(exclude_unset=True)
    
    if "autor_id" in update_data:
        autor = get_autor(db, update_data["autor_id"])
        if not autor:
            raise ValueError(f"Autor con ID {update_data['autor_id']} no existe")
    
    if "isbn" in update_data:
        isbn_clean = update_data["isbn"].replace('-', '').replace(' ', '')
        existing = get_libro_by_isbn(db, isbn_clean)
        if existing and existing.id != libro_id:
            raise ValueError(f"Libro con ISBN {isbn_clean} ya existe")
        update_data["isbn"] = isbn_clean
    
    for field, value in update_data.items():
        setattr(db_libro, field, value)
    
    db.commit()
    db.refresh(db_libro)
    
    return (
        db.query(models.Libro)
        .options(joinedload(models.Libro.autor))
        .filter(models.Libro.id == libro_id)
        .first()
    )


def delete_libro(db: Session, libro_id: int) -> bool:
    db_libro = get_libro(db, libro_id)
    if not db_libro:
        return False
    
    db.delete(db_libro)
    db.commit()
    return True

