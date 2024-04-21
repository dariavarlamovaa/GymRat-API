def test_login_user(test_client, first_superuser):
    response = test_client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin"
        },
    )
    user_data = response.json()
    print(user_data)
    assert response.status_code == 200
    assert 'access_token' in user_data
    assert user_data['token_type'] == 'bearer'


def test_not_allowed_to_login_with_wrong_password(test_client, first_inactive_user):
    response = test_client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "blablabla"
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_now_allowed_to_login_with_wrong_username(test_client, first_superuser):
    response = test_client.post(
        "/auth/login",
        data={
            "username": "another",
            "password": "admin"
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_not_allowed_to_login_inactive_user(test_client, first_inactive_user):
    response = test_client.post(
        "/auth/login",
        data={
            "username": "user1",
            "password": "111"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User is not active"


def test_signup_success(test_client):
    response = test_client.post(
        '/auth/signup',
        json={
            'username': 'admin',
            'email': 'admin@mail.com',
            'password': 'admin',
        },
    )
    assert response.status_code == 201


def test_now_allowed_to_signup_existing_user(test_client, first_superuser):
    user_data = {
        "username": "admin",
        "email": "admin@mail.com",
        "password": "admin",
    }
    response = test_client.post(
        "/auth/signup",
        json=user_data,
    )
    assert response.status_code == 409
    assert response.json()['detail'] == f'User with username or email already exists'
