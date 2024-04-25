from core.utils import _create_user
from security import create_access_token


def test_fetch_all_workouts(test_client, first_superuser, create_workout, valid_jwt_token):
    response = test_client.get('/workouts/all', headers=valid_jwt_token)
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = test_client.get('/workouts/all')
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"


def test_cant_fetch_workouts_if_not_super_user(test_client, first_user, create_workout, valid_jwt_token):
    response = test_client.get('/workouts/all', headers=valid_jwt_token)
    assert response.status_code == 403

    response = test_client.get('/workouts/all/2', headers=valid_jwt_token)
    assert response.status_code == 403


def test_fetch_one_workout(test_client, first_superuser, create_workout, valid_jwt_token):
    response = test_client.get('/workouts/all/1', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['name'] == 'workout1'

    response = test_client.get('/workouts/all/1')
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"


def test_fetch_my_workouts(test_client, first_user, create_workout, valid_jwt_token):
    response = test_client.get('/workouts/my', headers=valid_jwt_token)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_cant_fetch_workouts_if_nothing_in_a_storage(test_client, get_test_db, create_users):
    _create_user(get_test_db, 'second', 'second@mail.com', '111', True, False)
    second_jwt_token = create_access_token('2')
    response = test_client.get('/workouts/my', headers={"Authorization": f"Bearer {second_jwt_token}"})
    assert response.status_code == 404
    assert response.json()['detail'] == "You don`t have any workouts"


def test_fetch_my_one_workout(test_client, first_user, create_workout, valid_jwt_token):
    response = test_client.get('/workouts/my/1', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['expires'] == '2024-05-29'

    response = test_client.get('/workouts/my/2', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Workout with id - 2 not found in your storage"

    response = test_client.get('/workouts/name/workout1', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['name'] == 'workout1'

    response = test_client.get('/workouts/name/workout2', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Workout with name: 'workout2' not found"


def test_create_new_workout(test_client, first_user, valid_jwt_token):
    new_workout = {'name': 'test_workout', 'description': 'test_description', 'expires': '2024-06-05'}
    response = test_client.post('/workouts/create', headers=valid_jwt_token, json=new_workout)
    assert response.status_code == 201
    assert response.json()['name'] == 'test_workout'

    response = test_client.post('/workouts/create', headers=valid_jwt_token, json=new_workout)
    assert response.status_code == 409
    assert response.json()['detail'] == "Workout with name 'test_workout' already exists"

    response = test_client.post('/workouts/create', json=new_workout)
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"


def test_update_workout(test_client, first_user, valid_jwt_token, create_workout):
    updated_data = {'name': 'updated_name'}
    response = test_client.put('/workouts/update/1', headers=valid_jwt_token, json=updated_data)
    assert response.status_code == 200
    assert response.json()['name'] == 'updated_name'

    response = test_client.put('/workouts/update/2', headers=valid_jwt_token, json=updated_data)
    assert response.status_code == 404
    assert response.json()['detail'] == "Workout with id 2 not found"

    response = test_client.put('/workouts/update/2', json=updated_data)
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"


def test_delete_workout(test_client, first_user, valid_jwt_token, create_workout):
    response = test_client.delete('/workouts/delete/1', headers=valid_jwt_token)
    assert response.status_code == 200

    response = test_client.delete('/workouts/delete/2', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Workout with id 2 not found"

    response = test_client.delete('/workouts/delete/2')
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"


def test_fetch_exercises_from_workout(test_client, first_user, valid_jwt_token, create_workout):
    response = test_client.get('/workouts/1/exercises', headers=valid_jwt_token)
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = test_client.get('/workouts/2/exercises', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Workout with id 2 not found"

    response = test_client.get('/workouts/2/exercises')
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"


def test_add_exercise_to_workout(test_client, first_user, create_workout, create_exercises, valid_jwt_token):
    response = test_client.put('/workouts/1/add/1', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['name'] == 'workout1'

    response = test_client.put('/workouts/200/add/1', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Workout with id 200 not found"

    response = test_client.put('/workouts/1/add/200', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Exercise with id 200 not found"

    response = test_client.put('/workouts/2/add/1', headers=valid_jwt_token)
    assert response.status_code == 403
    assert response.json()['detail'] == "You don`t have permission to update this workout"

    response = test_client.put('/workouts/1/add/1', headers=valid_jwt_token)
    assert response.status_code == 409
    assert response.json()['detail'] == "Exercise is already in this workout"

    response = test_client.put('/workouts/1/add/1')
    assert response.status_code == 401


def test_remove_one_exercise_from_workout(test_client, first_user, create_workout, create_exercises, valid_jwt_token):
    response = test_client.put('/workouts/1/add/1', headers=valid_jwt_token)
    assert response.status_code == 200

    response = test_client.put('/workouts/1/remove/1', headers=valid_jwt_token)
    assert response.status_code == 200

    response = test_client.put('/workouts/200/remove/1', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Workout with id 200 not found"

    response = test_client.put('/workouts/1/remove/200', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Exercise with id 200 not found"

    response = test_client.put('/workouts/2/remove/1', headers=valid_jwt_token)
    assert response.status_code == 403
    assert response.json()['detail'] == "You don`t have permission to update this workout"

    response = test_client.put('/workouts/1/remove/3', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Exercise with id - 3 not in this workout"


def test_can_modify_workouts_if_super_user(test_client, first_superuser, valid_jwt_token, create_workout,
                                          create_exercises):
    new_workout = {'name': 'test_workout', 'description': 'test_description', 'expires': '2024-06-05'}
    response = test_client.post('/workouts/create', headers=valid_jwt_token, json=new_workout)
    assert response.status_code == 201
    assert response.json()['name'] == 'test_workout'

    updated_data = {'name': 'updated_name'}
    response = test_client.put('/workouts/update/1', headers=valid_jwt_token, json=updated_data)
    assert response.status_code == 200
    assert response.json()['name'] == 'updated_name'

    response = test_client.get('/workouts/1/exercises', headers=valid_jwt_token)
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = test_client.put('/workouts/1/add/1', headers=valid_jwt_token)
    assert response.status_code == 200

    response = test_client.put('/workouts/1/remove/1', headers=valid_jwt_token)
    assert response.status_code == 200

    response = test_client.delete('/workouts/delete/1', headers=valid_jwt_token)
    assert response.status_code == 200
