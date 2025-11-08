import pytest
from fastapi import status
from app import crud, schemas


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"


def test_create_libro_success(client, sample_autor_data, sample_libro_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    response = client.post("/libros", json=sample_libro_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["titulo"] == sample_libro_data["titulo"]
    assert data["isbn"] == sample_libro_data["isbn"].replace('-', '').replace(' ', '')
    assert data["autor_id"] == db_autor.id


def test_create_libro_duplicate_isbn(client, sample_autor_data, sample_libro_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    response1 = client.post("/libros", json=sample_libro_data)
    assert response1.status_code == status.HTTP_201_CREATED
    
    response2 = client.post("/libros", json=sample_libro_data)
    assert response2.status_code == status.HTTP_409_CONFLICT


def test_create_libro_invalid_data(client):
    invalid_data = {
        "titulo": "",
        "isbn": "123",
        "ano_publicacion": 500,
        "autor_id": 1
    }
    response = client.post("/libros", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_libro_success(client, sample_autor_data, sample_libro_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    response = client.get(f"/libros/{db_libro.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == db_libro.id
    assert data["titulo"] == sample_libro_data["titulo"]


def test_get_libro_not_found(client):
    response = client.get("/libros/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_libros(client, sample_autor_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Libro 1", "isbn": "1234567890", "ano_publicacion": 2000, "autor_id": db_autor.id},
        {"titulo": "Libro 2", "isbn": "0987654321", "ano_publicacion": 2001, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    response = client.get("/libros")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) == 2


def test_list_libros_with_filters(client, sample_autor_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Libro 1", "isbn": "1234567890", "ano_publicacion": 2000, "autor_id": db_autor.id},
        {"titulo": "Libro 2", "isbn": "0987654321", "ano_publicacion": 2001, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    response = client.get("/libros?ano=2000")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["ano_publicacion"] == 2000


def test_list_libros_pagination(client, sample_autor_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    for i in range(15):
        libro_data = {
            "titulo": f"Libro {i}",
            "isbn": f"9781234567{i:03d}",
            "ano_publicacion": 2000 + i,
            "autor_id": db_autor.id
        }
        crud.create_libro(db=db, libro=schemas.LibroCreate(**libro_data))
    
    response = client.get("/libros?skip=0&limit=10")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 10
    
    response = client.get("/libros?skip=10&limit=10")
    assert len(response.json()["items"]) == 5


def test_update_libro_success(client, sample_autor_data, sample_libro_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    update_data = {"titulo": "Nuevo título"}
    response = client.put(f"/libros/{db_libro.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["titulo"] == "Nuevo título"


def test_update_libro_not_found(client):
    update_data = {"titulo": "Nuevo título"}
    response = client.put("/libros/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_libro_success(client, sample_autor_data, sample_libro_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    response = client.delete(f"/libros/{db_libro.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    response = client.get(f"/libros/{db_libro.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_libro_not_found(client):
    response = client.delete("/libros/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_search_libros_by_titulo(client, sample_autor_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Cien años de soledad", "isbn": "1234567890", "ano_publicacion": 1967, "autor_id": db_autor.id},
        {"titulo": "El amor en los tiempos del cólera", "isbn": "0987654321", "ano_publicacion": 1985, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    response = client.get("/libros/buscar?titulo=soledad")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert "soledad" in data["items"][0]["titulo"].lower()


def test_search_libros_by_autor(client, sample_autor_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Libro 1", "isbn": "1234567890", "ano_publicacion": 1967, "autor_id": db_autor.id},
        {"titulo": "Libro 2", "isbn": "0987654321", "ano_publicacion": 1985, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    response = client.get("/libros/buscar?autor=García")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 2


def test_search_libros_no_params(client):
    response = client.get("/libros/buscar")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_libro_duplicate_isbn(client, sample_autor_data, sample_libro_data, db):
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
    
    response = client.put(f"/libros/{db_libro1.id}", json={"isbn": db_libro2.isbn})
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_libro_invalid_autor(client, sample_autor_data, sample_libro_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    sample_libro_data["autor_id"] = db_autor.id
    libro = schemas.LibroCreate(**sample_libro_data)
    db_libro = crud.create_libro(db=db, libro=libro)
    
    response = client.put(f"/libros/{db_libro.id}", json={"autor_id": 999})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_libros_with_autor_id_filter(client, sample_autor_data, db):
    autor = schemas.AutorCreate(**sample_autor_data)
    db_autor = crud.create_autor(db=db, autor=autor)
    
    libros_data = [
        {"titulo": "Libro 1", "isbn": "1234567890", "ano_publicacion": 2000, "autor_id": db_autor.id},
        {"titulo": "Libro 2", "isbn": "0987654321", "ano_publicacion": 2001, "autor_id": db_autor.id},
    ]
    
    for libro_data in libros_data:
        libro = schemas.LibroCreate(**libro_data)
        crud.create_libro(db=db, libro=libro)
    
    response = client.get(f"/libros?autor_id={db_autor.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 2

