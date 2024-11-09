# import pytest
# from src.librairie import app, jsonify


# @pytest.fixture
# def test_app():
#     app.config.update(
#         {
#             "TESTING": True,
#         }
#     )
#     return app


# @pytest.fixture
# def client(test_app):
#     return test_app.test_client()

# def test_put(client):
#     response = client.post('/books', json={
#         'title': 'La vie de brian',
#         'author': 'Monty Python)',
#         'stock': 25,
#     })
#     id = response.get_json()['id']
#     client.put(f'/books/{id}', json={
#         'title': 'La vie de brian',
#         'author': 'Monty Python)',
#         'stock': 30,
#     })
#     assert client.get(f'/books/{id}').get_json()['stock'] == 30

# def fake_execute(request, args):
#     pass

# def test_borrow_with_mock(mocker, client):
#     mock_db = mocker.patch('src.librairie.get_existing_or_create_db')
#     mock_cursor = mocker.MagicMock()
#     mock_cursor.fetchone.return_value = (1,) # return value doit etre "subscriptable", par exemple un tuple
#     mock_cursor.execute = fake_execute
#     mock_db.return_value.cursor.return_value = mock_cursor
#     response = client.post('/books/1/borrow')
#     assert response.status_code == 200


