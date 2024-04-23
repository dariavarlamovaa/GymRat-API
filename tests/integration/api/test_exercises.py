def test_fetch_all_exercises(test_client, first_superuser, valid_jwt_token, create_exercises):
    response = test_client.get('/exercises/all', headers=valid_jwt_token)
    assert response.status_code == 200 and len(response.json()) == 3

    response = test_client.get('/exercises/all')
    assert response.status_code == 401


def test_fetch_one_exercise(test_client, first_superuser, valid_jwt_token, create_exercises):
    response = test_client.get('/exercises/all/1', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['title'] == 'testex1'

    response = test_client.get('/exercises/all/4', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == 'Exercise with id - 4 not found'

    response = test_client.get('/exercises/title/testex1', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['exercise_id'] == 1

    response = test_client.get('/exercises/title/wrong', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Exercise with title: 'wrong' not found"


def test_cant_fetch_exercises_if_not_superuser(test_client, first_user, valid_jwt_token, create_exercises):
    response = test_client.get('/exercises/all', headers=valid_jwt_token)
    assert response.status_code == 403

    response = test_client.get('/exercises/all/1', headers=valid_jwt_token)
    assert response.status_code == 403

    response = test_client.get('/exercises/title/testex1', headers=valid_jwt_token)
    assert response.status_code == 403


def test_fetch_my_exercises(test_client, first_user, valid_jwt_token, create_exercises):
    response = test_client.get('/exercises/my')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'

    response = test_client.get('/exercises/my', headers=valid_jwt_token)
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = test_client.get('/exercises/my/3', headers=valid_jwt_token)
    assert response.status_code == 200
    assert response.json()['title'] == 'testex3'

    response = test_client.get('/exercises/my/2', headers=valid_jwt_token)
    assert response.status_code == 404
    assert response.json()['detail'] == "Exercise with id - 2 not found in your storage"


def test_create_new_exercise(test_client, first_user, valid_jwt_token):
    new_exercise = {'title': 'testex4', 'equipment': 'testeq', 'muscle': 'full_body', 'exercise_type': 'cardio',
                    'level': 'intermediate'}

    response = test_client.post('/exercises/create',
                                json=new_exercise,
                                headers=valid_jwt_token
                                )
    assert response.status_code == 201
    assert response.json()['title'] == 'testex4'

    response = test_client.post('/exercises/create', json=new_exercise)
    assert response.status_code == 401


def test_update_exercise(test_client, first_user, create_exercises, valid_jwt_token):
    new_data = {'title': 'updatedtitle1'}

    response = test_client.put('/exercises/update/1',
                               json=new_data,
                               headers=valid_jwt_token
                               )
    assert response.status_code == 200
    assert response.json()['title'] == 'updatedtitle1'

    response = test_client.put('/exercises/update/1', json=new_data)
    assert response.status_code == 401

    response = test_client.put('/exercises/update/100',
                               json=new_data,
                               headers=valid_jwt_token
                               )
    assert response.status_code == 404

    response = test_client.put('/exercises/update/2',
                               json=new_data,
                               headers=valid_jwt_token
                               )
    assert response.status_code == 403


def test_delete_exercise(test_client, first_user, create_exercises, valid_jwt_token):
    response = test_client.delete('/exercises/delete/1', headers=valid_jwt_token)
    assert response.status_code == 200

    response = test_client.delete('/exercises/delete/1')
    assert response.status_code == 401

    response = test_client.delete('/exercises/delete/100', headers=valid_jwt_token)
    assert response.status_code == 404

    response = test_client.delete('/exercises/delete/2', headers=valid_jwt_token)
    assert response.status_code == 403


def test_can_modify_exercises_if_super_user(test_client, first_superuser, valid_jwt_token, create_exercises):
    new_exercise = {'title': 'testex4', 'equipment': 'testeq', 'muscle': 'full_body', 'exercise_type': 'cardio',
                    'level': 'intermediate'}

    response = test_client.post('/exercises/create',
                                json=new_exercise,
                                headers=valid_jwt_token
                                )
    assert response.status_code == 201
    assert response.json()['title'] == 'testex4'

    new_data = {'title': 'updatedtitle1'}

    response = test_client.put('/exercises/update/1',
                               json=new_data,
                               headers=valid_jwt_token
                               )
    assert response.status_code == 200
    assert response.json()['title'] == 'updatedtitle1'

    response = test_client.delete('/exercises/delete/1', headers=valid_jwt_token)
    assert response.status_code == 200
