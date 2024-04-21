import pytest

from core.utils import _create_user


@pytest.fixture
def create_users(get_test_db):
    _create_user(get_test_db, 'test1', 'test1@mail.com', '111',
                 True, False)
    _create_user(get_test_db, 'test2', 'test2@mail.com', '111',
                 True, False)


def test_fetch_all_users(test_client, first_superuser, create_users, valid_jwt_token):
    response = test_client.get('/users/all', headers=valid_jwt_token)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_not_allowed_to_fetch_all_users_if_not_superuser(test_client, first_user, valid_jwt_token):
    response = test_client.get('/users/all', headers=valid_jwt_token)
    assert response.status_code == 403


def test_not_allowed_to_fetch_all_users_if_not_authenticated(test_client):
    response = test_client.get('/users/all')
    assert response.status_code == 401


def test_fetch_user_by_id(test_client, first_superuser, create_users, valid_jwt_token):
    response = test_client.get('/users/all/2', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['user_id'] == 2

    response = test_client.get('/users/all/105', headers=valid_jwt_token)
    assert response.status_code == 404


def test_fetch_user_by_username(test_client, first_superuser, create_users, valid_jwt_token):
    response = test_client.get('/users/username/test1', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['username'] == 'test1'

    response = test_client.get('/users/username/test111', headers=valid_jwt_token)
    assert response.status_code == 404


def test_fetch_user_by_email(test_client, first_superuser, create_users, valid_jwt_token):
    response = test_client.get('/users/email/test1@mail.com', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['email'] == 'test1@mail.com'

    response = test_client.get('/users/email/test111@mail.com', headers=valid_jwt_token)
    assert response.status_code == 404


def test_create_new_user(test_client, first_superuser, valid_jwt_token):
    response = test_client.post('/users/create', json={
        'username': 'testcreate',
        'email': 'testcreate@mail.com',
        'hashed_password': 'testcreate'
    }, headers=valid_jwt_token)
    assert response.status_code == 201

    response = test_client.post('/users/create', json={
        'username': 'testcreate',
        'email': 'testcreate@mail.com',
        'hashed_password': 'testcreate'
    }, headers=valid_jwt_token)
    assert response.status_code == 409

    response = test_client.post('/users/create', json={
        'username': 'testcreate',
        'hashed_password': 'testcreate'
    }, headers=valid_jwt_token)
    assert response.status_code == 422

    response = test_client.post('/users/create', json={
        'username': 'testcreate',
        'email': 'testcreate@mail.com',
        'hashed_password': 'testcreate'
    })
    assert response.status_code == 401


def test_delete_one_user(test_client, first_superuser, create_users, valid_jwt_token):
    response = test_client.delete('/users/delete/2', headers=valid_jwt_token)
    assert response.status_code == 200

    response = test_client.delete('/users/delete/1', headers=valid_jwt_token)
    assert response.status_code == 403

    response = test_client.delete('/users/delete/105', headers=valid_jwt_token)
    assert response.status_code == 404


def test_delete_if_normal_user(test_client, first_user, create_users, valid_jwt_token):
    response = test_client.delete('/users/delete/2', headers=valid_jwt_token)
    assert response.status_code == 403

    response = test_client.delete('/users/delete/1', headers=valid_jwt_token)
    assert response.status_code == 200


def test_update_one_user(test_client, first_superuser, create_users, valid_jwt_token):
    data = {'is_superuser': True}
    response = test_client.put('/users/update/2', headers=valid_jwt_token, json=data)
    assert response.status_code == 200
    assert response.json()['is_superuser'] is True

    response = test_client.put('/users/update/105', headers=valid_jwt_token, json=data)
    assert response.status_code == 404

    password = {'hashed_password': '111'}
    response = test_client.put('/users/update/2', headers=valid_jwt_token, json=password)
    assert response.status_code == 200


def test_fetch_user_me(test_client, first_user, valid_jwt_token):
    response = test_client.get('/users/me', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['username'] == 'user1'


def test_update_my_data(test_client, first_user, valid_jwt_token):
    data = {'username': 'user11'}
    response = test_client.put('/users/update-my-data', headers=valid_jwt_token, json=data)
    assert response.status_code == 200
    assert response.json()['username'] == 'user11'

    data = {'email': 'user11@mail.com'}
    response = test_client.put('/users/update-my-data', headers=valid_jwt_token, json=data)
    assert response.status_code == 200
    assert response.json()['email'] == 'user11@mail.com'


def test_update_my_password(test_client, first_user, valid_jwt_token):
    data = {'new_password': '123', 'current_password': '111'}
    response = test_client.patch('/users/update-my-password', headers=valid_jwt_token, json=data)
    assert response.status_code == 200

    data = {'new_password': '111', 'current_password': '111'}
    response = test_client.patch('/users/update-my-password', headers=valid_jwt_token, json=data)
    assert response.status_code == 409
