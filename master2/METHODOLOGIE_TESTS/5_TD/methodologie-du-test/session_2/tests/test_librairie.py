import pytest
from src.librairie import app, jsonify


@pytest.fixture
def test_app():
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_post(client) -> None:
    response = client.post(
        "/books",
        json={"title": "1984", "author": "George Orwell", "year": 1949, "stock": 8},
    )
    json = response.get_json()
    id = json["id"]
    assert response.status_code == 201
    assert json["title"] == "1984"
    assert json == {
        "id": id,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "stock": 8,
    }


def test_borrow(client) -> None:
    response = client.post(
        "/books",
        json={"title": "1984", "author": "George Orwell", "year": 1949, "stock": 1},
    )
    json = response.get_json()
    id = json["id"]

    borrow_response = client.post(f"/books/{id}/borrow")
    assert borrow_response.status_code == 200
    borrow_response = client.post(f"/books/{id}/borrow")
    assert borrow_response.status_code == 400


def test_borrow_book_with_mock(mocker, client) -> None:
    mock_db = mocker.patch("src.librairie.get_existing_or_create_db")
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = {
        0: 1,
        1: "titre",
        2: "auteur",
        3: 1234,
        4: 25,
    }  # return value doit etre "subscriptable", par exemple un tuple
    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.get("/books/1")
    json = response.get_json()
    assert 1 == json["id"]
