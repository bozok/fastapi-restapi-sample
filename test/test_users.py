from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_get_users(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == 'bozok17@gmail.com'


def test_change_password(test_user):
    response = client.put("/user/change-password", json={"password": "mypassword", 'new_password': 'mynewpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change-password", json={"password": "wrong_password", 'new_password': 'mynewpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Error on password change'


def test_change_phone_number(test_user):
    response = client.put("/user/phone-number/+90mynewpassword")
    assert response.status_code == status.HTTP_204_NO_CONTENT