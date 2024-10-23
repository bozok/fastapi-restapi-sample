from fastapi import status

from routers.todos import get_db, get_current_user

from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all_todos(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['completed'] is False
    assert response.json()[0]['title'] == 'Learn to code'
    assert response.json()[0]['description'] == 'Need to learn everyday!'
    assert response.json()[0]['user_id'] == 1


def test_get_todo(test_todo):
    response = client.get('/todos/1')
    assert response.status_code == status.HTTP_200_OK


def test_get_todo_not_found(test_todo):
    response = client.get('/todos/2')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_new_todo(test_todo):
    request_data = {
        'title': 'New todo',
        'description':"New todo description",
        'priority': 5,
        'completed': False
    }
    response = client.post('/todos', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.pkid == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.completed is False


def test_update_todo(test_todo):
    request_data = {
        'title': 'Change the title fo the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'completed': False
    }

    response = client.put('/todos/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.pkid == 1).first()
    assert model.title == request_data.get('title')


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Change the title fo the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'completed': False
    }

    response = client.put('/todos/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.pkid == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}