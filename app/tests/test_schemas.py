import pytest
from datetime import datetime
from pydantic import ValidationError
from app import schemas


def test_autor_create_valid():
    autor = schemas.AutorCreate(nombre="Gabriel García Márquez")
    assert autor.nombre == "Gabriel García Márquez"


def test_autor_create_invalid_empty():
    with pytest.raises(ValidationError):
        schemas.AutorCreate(nombre="")


def test_autor_create_invalid_too_long():
    nombre_largo = "a" * 201
    with pytest.raises(ValidationError):
        schemas.AutorCreate(nombre=nombre_largo)


def test_libro_create_valid():
    libro = schemas.LibroCreate(
        titulo="Cien años de soledad",
        isbn="9788437604947",
        ano_publicacion=1967,
        autor_id=1
    )
    assert libro.titulo == "Cien años de soledad"
    assert libro.isbn == "9788437604947"
    assert libro.ano_publicacion == 1967


def test_isbn_valid_10_digits():
    libro = schemas.LibroCreate(
        titulo="Test",
        isbn="1234567890",
        ano_publicacion=2000,
        autor_id=1
    )
    assert libro.isbn == "1234567890"


def test_isbn_valid_13_digits():
    libro = schemas.LibroCreate(
        titulo="Test",
        isbn="9788437604947",
        ano_publicacion=2000,
        autor_id=1
    )
    assert libro.isbn == "9788437604947"


def test_isbn_valid_with_dashes():
    libro = schemas.LibroCreate(
        titulo="Test",
        isbn="978-84-376-0494-7",
        ano_publicacion=2000,
        autor_id=1
    )
    assert libro.isbn == "9788437604947"


def test_isbn_invalid_length():
    with pytest.raises(ValidationError, match="ISBN debe tener 10 o 13 dígitos"):
        schemas.LibroCreate(
            titulo="Test",
            isbn="12345",
            ano_publicacion=2000,
            autor_id=1
        )


def test_isbn_invalid_characters():
    with pytest.raises(ValidationError, match="ISBN debe contener solo dígitos"):
        schemas.LibroCreate(
            titulo="Test",
            isbn="978843760494X",
            ano_publicacion=2000,
            autor_id=1
        )


def test_ano_publicacion_valid():
    ano_actual = datetime.now().year
    libro = schemas.LibroCreate(
        titulo="Test",
        isbn="1234567890",
        ano_publicacion=ano_actual,
        autor_id=1
    )
    assert libro.ano_publicacion == ano_actual


def test_ano_publicacion_invalid_too_old():
    with pytest.raises(ValidationError, match="Año de publicación debe ser mayor a 1000"):
        schemas.LibroCreate(
            titulo="Test",
            isbn="1234567890",
            ano_publicacion=500,
            autor_id=1
        )


def test_ano_publicacion_invalid_future():
    ano_futuro = datetime.now().year + 1
    with pytest.raises(ValidationError, match="Año de publicación no puede ser mayor"):
        schemas.LibroCreate(
            titulo="Test",
            isbn="1234567890",
            ano_publicacion=ano_futuro,
            autor_id=1
        )


def test_titulo_invalid_empty():
    with pytest.raises(ValidationError):
        schemas.LibroCreate(
            titulo="",
            isbn="1234567890",
            ano_publicacion=2000,
            autor_id=1
        )


def test_titulo_invalid_too_long():
    titulo_largo = "a" * 301
    with pytest.raises(ValidationError):
        schemas.LibroCreate(
            titulo=titulo_largo,
            isbn="1234567890",
            ano_publicacion=2000,
            autor_id=1
        )


def test_libro_update_partial():
    libro_update = schemas.LibroUpdate(titulo="Nuevo título")
    assert libro_update.titulo == "Nuevo título"
    assert libro_update.isbn is None


def test_libro_update_all_fields():
    libro_update = schemas.LibroUpdate(
        titulo="Nuevo título",
        isbn="9876543210",
        ano_publicacion=2020,
        autor_id=2
    )
    assert libro_update.titulo == "Nuevo título"
    assert libro_update.isbn == "9876543210"
    assert libro_update.ano_publicacion == 2020
    assert libro_update.autor_id == 2


def test_isbn_empty_string():
    with pytest.raises(ValidationError):
        schemas.LibroCreate(
            titulo="Test",
            isbn="",
            ano_publicacion=2000,
            autor_id=1
        )


def test_libro_update_empty():
    with pytest.raises(ValidationError, match="Al menos un campo"):
        schemas.LibroUpdate()


def test_libro_update_isbn_none():
    libro_update = schemas.LibroUpdate(titulo="Nuevo título", isbn=None)
    assert libro_update.isbn is None


def test_libro_update_ano_none():
    libro_update = schemas.LibroUpdate(titulo="Nuevo título", ano_publicacion=None)
    assert libro_update.ano_publicacion is None


def test_libro_update_isbn_invalid_characters():
    with pytest.raises(ValidationError, match="ISBN debe contener solo dígitos"):
        schemas.LibroUpdate(isbn="978843760494X")


def test_libro_update_isbn_invalid_length():
    with pytest.raises(ValidationError, match="ISBN debe tener 10 o 13 dígitos"):
        schemas.LibroUpdate(isbn="12345")


def test_libro_update_ano_too_old():
    with pytest.raises(ValidationError, match="Año de publicación debe ser mayor a 1000"):
        schemas.LibroUpdate(ano_publicacion=500)


def test_libro_update_ano_future():
    ano_futuro = datetime.now().year + 1
    with pytest.raises(ValidationError, match="Año de publicación no puede ser mayor"):
        schemas.LibroUpdate(ano_publicacion=ano_futuro)

