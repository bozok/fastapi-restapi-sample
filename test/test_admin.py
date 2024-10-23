from fastapi import status

from .utils import *

from routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_all_todos(test_todo):
    response = client.get('/admin/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['completed'] is False
    assert response.json()[0]['title'] == 'Learn to code'
    assert response.json()[0]['description'] == 'Need to learn everyday!'
    assert response.json()[0]['user_id'] == 1
    assert response.json()[0]['pkid'] == 1



def test_delete_todo(test_todo):
    response = client.delete('/admin/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.pkid == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete('/admin/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND