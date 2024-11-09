import pytest
from src.tasks import app, jsonify


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

def test_activate_past_task(client):
    response = client.post('/tasks', json={
        "title": "Marty, Pense a nourrir le chat",
        "description": "Penser a nourrir le chat avant de partir vers le futur",
        "due_date": "1985−10−30",
        "priority": 1,
        "difficulty": 10
    })
    assert client.get(f'/tasks/active').get_json()['message'] == 'Aucune tâche active trouvée.'
    id = response.get_json()['id']
    response = client.post(f'/tasks/{id}/complete')
    assert response.status_code == 200


def test_create_task_without_date(client):
    response = client.post('/tasks', json={
        "title": "Un jour mon prince viendra",
        "description": "Trouve toi un boulot, plutôt...",
        "due_date": None,
        "priority": 1,
        "difficulty": 10
    })
    assert response.status_code == 201

def test_create_task_without_title(client):
    response = client.post('/tasks', json={
        "description": "Untitled",
        "due_date": "2024−12−20",
        "priority": 1,
        "difficulty": 10
    })
    assert response.status_code == 400

def test_activate_one_task(client):
    response = client.post('/tasks', json={
        "title": "Repasser les chausettes",
        "description": "Consiste a repasser les 2 chausettes dedans et dehors",
        "due_date": "2024−12−20",
        "priority": 1,
        "difficulty": 2
    })
    id = response.get_json()['id']
    tasks_active = client.get(f'/tasks/active').get_json()
    new_create_active_task = next((item for item in tasks_active if item["id"] == id), None)
    potential_result = {
        'completed': 0,
        'description': 'Consiste a repasser les 2 chausettes dedans et dehors',
        'difficulty': 2, 'due_date': '2024−12−20',
        'id': id,
        'priority': 1,
        'title': 'Repasser les chausettes',
        'worth': 20
    }
    assert potential_result == new_create_active_task


def test_complete_one_task(client):
    client.delete('/tasks/cleanup')
    response = client.post('/tasks', json={
        "title": "Finir le packet de chips",
        "description": "Finaliser le packet de chips et manger les miettes",
        "due_date": "2024−12−18",
        "priority": 3,
        "difficulty": 2
    })
    id = response.get_json()['id']
    client.post(f'/tasks/{id}/complete')
    assert client.delete('/tasks/cleanup').get_json()['message'] == "1 tâches obsolètes ou complétées supprimées"
    response = client.post(f'/tasks/{id}/complete')
    assert response.status_code == 404


def test_complete_task_with_inexisting_id(client):
    response = client.post(f'/tasks/15487845854585/complete')
    assert response.status_code == 404

def test_incremente_score(client):
    score_before = client.get('/scores/total').get_json()['total_score']
    print(score_before)
    response = client.post('/tasks', json={
        "title": "Une fausse tache pour fainéantiser 1 heure",
        "description": "Consiste a finaliser un faux ticket pour montrer que... ca bosse",
        "due_date": "2024−12−25",
        "priority": 3,
        "difficulty": 2
    })
    id = response.get_json()['id']
    client.post(f'/tasks/{id}/complete')
    score_after = client.get('/scores/total').get_json()['total_score']
    assert score_after == score_before + 60

def test_complete_all_active_tasks(client):
    tasks_active = client.get(f'/tasks/active').get_json()
    for task in tasks_active:
        client.post(f'/tasks/{task["id"]}/complete')
    assert client.get(f'/tasks/active').get_json()['message'] == 'Aucune tâche active trouvée.'


def test_incremente_score_with_mock(mocker, client):
    mock_db = mocker.patch('src.tasks.get_existing_or_create_db')
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = {'completed': 0, 'priority':1, 'difficulty': 1, 'due_date':"2024−12−25"} # return value doit etre "subscriptable", par exemple un tuple
    mock_cursor.execute = fake_execute
    mock_db.return_value.cursor.return_value = mock_cursor
    response = client.post(f'/tasks/1/complete')
    assert response.status_code == 200

def fake_execute(request, args):
    pass
