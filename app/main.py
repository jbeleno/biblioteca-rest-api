from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas
from app.database import get_db, init_db


def _to_http_error(e: ValueError):
    msg = str(e)
    if "ISBN" in msg and "ya existe" in msg:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    if "no existe" in msg:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


def _serialize_libros(libros):
    return [schemas.LibroResponse.model_validate(libro).model_dump() for libro in libros]


app = FastAPI(
    title="Biblioteca API",
    description="API REST para gestionar una biblioteca con libros y autores",
    version="1.0.0"
)

# Configurar CORS
# En producción, reemplazar allow_origins=["*"] con una lista específica de orígenes permitidos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: ["https://tudominio.com", "https://www.tudominio.com"]
    allow_credentials=True,
    allow_methods=["*"],  # En producción: ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "message": "API is running"}


@app.post(
    "/libros",
    response_model=schemas.LibroResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Libros"]
)
def create_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    try:
        db_libro = crud.create_libro(db=db, libro=libro)
        return schemas.LibroResponse.model_validate(db_libro)
    except ValueError as e:
        _to_http_error(e)


@app.get("/libros", response_model=dict, tags=["Libros"])
def list_libros(
    autor_id: Optional[int] = Query(None),
    ano: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    libros = crud.get_libros(db=db, skip=skip, limit=limit, autor_id=autor_id, ano=ano)
    total = crud.count_libros(db=db, autor_id=autor_id, ano=ano)
    
    items = _serialize_libros(libros)
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@app.get("/libros/buscar", response_model=dict, tags=["Libros"])
def search_libros(
    titulo: Optional[str] = Query(default=None),
    autor: Optional[str] = Query(default=None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    titulo = titulo.strip() if titulo and titulo.strip() else None
    autor = autor.strip() if autor and autor.strip() else None
    
    if not titulo and not autor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere al menos titulo o autor"
        )
    
    libros = crud.search_libros(db=db, titulo=titulo, autor=autor, skip=skip, limit=limit)
    total = crud.count_search_libros(db=db, titulo=titulo, autor=autor)
    
    items = _serialize_libros(libros)
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@app.get("/libros/{libro_id}", response_model=schemas.LibroResponse, tags=["Libros"])
def get_libro(libro_id: int, db: Session = Depends(get_db)):
    db_libro = crud.get_libro(db=db, libro_id=libro_id)
    if db_libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return schemas.LibroResponse.model_validate(db_libro)


@app.put("/libros/{libro_id}", response_model=schemas.LibroResponse, tags=["Libros"])
def update_libro(libro_id: int, libro_update: schemas.LibroUpdate, db: Session = Depends(get_db)):
    try:
        db_libro = crud.update_libro(db=db, libro_id=libro_id, libro_update=libro_update)
        if db_libro is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Libro con ID {libro_id} no encontrado"
            )
        return schemas.LibroResponse.model_validate(db_libro)
    except ValueError as e:
        _to_http_error(e)


@app.delete("/libros/{libro_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Libros"])
def delete_libro(libro_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_libro(db=db, libro_id=libro_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return None

