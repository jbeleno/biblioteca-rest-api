import pytest
from app import crud, schemas, models


def test_create_autor(db, sample_autor_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    assert db_autor.id is not None
    assert db_autor.nombre == sample_autor_data["nombre"]


def test_get_autor(db, sample_autor_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    retrieved_autor = crud.get_autor(db=db, autor_id=db_autor.id)
    assert retrieved_autor is not None
    assert retrieved_autor.nombre == sample_autor_data["nombre"]


def test_get_autor_by_nombre(db, sample_autor_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    retrieved_autor = crud.get_autor_by_nombre(db=db, nombre=sample_autor_data["nombre"])
    assert retrieved_autor is not None
    assert retrieved_autor.id == db_autor.id


def test_create_libro(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    assert db_libro.id is not None
    assert db_libro.titulo == sample_libro_data["titulo"]
    assert db_libro.isbn == sample_libro_data["isbn"].replace('-', '').replace(' ', '')
    assert db_libro.autor_id == db_autor.id


def test_create_libro_duplicate_isbn(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    crud.create_libro(db=db, libro=libro)
    
    with pytest.raises(ValueError, match="ISBN.*ya existe"):
        crud.create_libro(db=db, libro=libro)


def test_create_libro_invalid_autor(db, sample_libro_data):
    sample_libro_data["autor_id"] = 999
    libro = schemas.LibroCreate(**sample_libro_data)
    
    with pytest.raises(ValueError, match="Autor.*no existe"):
        crud.create_libro(db=db, libro=libro)


def test_get_libro(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    retrieved_libro = crud.get_libro(db=db, libro_id=db_libro.id)
    assert retrieved_libro is not None
    assert retrieved_libro.titulo == sample_libro_data["titulo"]


def test_get_libros_with_filters(db, sample_autor_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Libro 1", "isbn": "1234567890", "ano_publicacion": 2000, "autor_id": db_autor.id},
        {"titulo": "Libro 2", "isbn": "0987654321", "ano_publicacion": 2001, "autor_id": db_autor.id},
        {"titulo": "Libro 3", "isbn": "1122334455", "ano_publicacion": 2000, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    libros_2000 = crud.get_libros(db=db, ano=2000)
    assert len(libros_2000) == 2
    
    libros_autor = crud.get_libros(db=db, autor_id=db_autor.id)
    assert len(libros_autor) == 3


def test_update_libro(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    libro_update = schemas.LibroUpdate(titulo="Nuevo título")
    updated_libro = crud.update_libro(db=db, libro_id=db_libro.id, libro_update=libro_update)
    
    assert updated_libro.titulo == "Nuevo título"
    assert updated_libro.isbn == db_libro.isbn


def test_update_libro_with_new_isbn(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    nuevo_isbn = "9876543210"
    libro_update = schemas.LibroUpdate(isbn=nuevo_isbn)
    updated_libro = crud.update_libro(db=db, libro_id=db_libro.id, libro_update=libro_update)
    
    assert updated_libro.isbn == nuevo_isbn


def test_delete_libro(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    deleted = crud.delete_libro(db=db, libro_id=db_libro.id)
    assert deleted is True
    
    retrieved_libro = crud.get_libro(db=db, libro_id=db_libro.id)
    assert retrieved_libro is None


def test_search_libros(db, sample_autor_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Cien años de soledad", "isbn": "1234567890", "ano_publicacion": 1967, "autor_id": db_autor.id},
        {"titulo": "El amor en los tiempos del cólera", "isbn": "0987654321", "ano_publicacion": 1985, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    resultados = crud.search_libros(db=db, titulo="soledad")
    assert len(resultados) == 1
    assert resultados[0].titulo == "Cien años de soledad"
    
    resultados = crud.search_libros(db=db, autor="García")
    assert len(resultados) == 2


def test_count_libros_with_autor_id(db, sample_autor_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Libro 1", "isbn": "1234567890", "ano_publicacion": 2000, "autor_id": db_autor.id},
        {"titulo": "Libro 2", "isbn": "0987654321", "ano_publicacion": 2001, "autor_id": db_autor.id},
        {"titulo": "Libro 3", "isbn": "1122334455", "ano_publicacion": 2000, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    count = crud.count_libros(db=db, autor_id=db_autor.id)
    assert count == 3


def test_update_libro_invalid_autor(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    libro_update = schemas.LibroUpdate(autor_id=999)
    with pytest.raises(ValueError, match="Autor.*no existe"):
        crud.update_libro(db=db, libro_id=db_libro.id, libro_update=libro_update)


def test_update_libro_duplicate_isbn(db, sample_autor_data, sample_libro_data):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro1_data = sample_libro_data.copy()
    libro1 = schemas.LibroCreate(**libro1_data)
    db_libro1 = crud.create_libro(db=db, libro=libro1)
    
    libro2_data = sample_libro_data.copy()
    libro2_data["isbn"] = "9876543210"
    libro2 = schemas.LibroCreate(**libro2_data)
    db_libro2 = crud.create_libro(db=db, libro=libro2)
    
    libro_update = schemas.LibroUpdate(isbn=db_libro2.isbn)
    with pytest.raises(ValueError, match="ISBN.*ya existe"):
        crud.update_libro(db=db, libro_id=db_libro1.id, libro_update=libro_update)

