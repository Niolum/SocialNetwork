import json

import pytest


pytestmark = pytest.mark.asyncio


async def test_create_user(async_client):
    test_request_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    response = await async_client.post("/users/signup", content=json.dumps(test_request_payload))
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["username"] == "test_user"
    assert response.json()["email"] == "test@mail.ru"
    assert response.json()["created_at"] is not None
    assert response.json()["full_name"] is None
    assert response.json()["given_name"] is None
    assert response.json()["family_name"] is None
    assert response.json()["location"] is None
    assert response.json()["avatar"] is None


async def test_create_user_username_exists(async_client):
    test_request_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_second_request_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_response_payload = {"detail": "Username is already exists"}
    response = await async_client.post("/users/signup", content=json.dumps(test_request_payload))
    response = await async_client.post("/users/signup", content=json.dumps(test_second_request_payload))

    assert response.status_code == 400
    assert response.json() == test_response_payload


async def test_create_user_email_exists(async_client):
    test_request_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_second_request_payload = {
        "username": "another_test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_response_payload = {"detail": "Email is already exists"}
    response = await async_client.post("/users/signup", content=json.dumps(test_request_payload))
    response = await async_client.post("/users/signup", content=json.dumps(test_second_request_payload))

    assert response.status_code == 400
    assert response.json() == test_response_payload


async def test_login(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None


async def test_login_incorrect(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    incorrect_data = {"username": "test_user", "password": "qwe"}
    test_answer = {'detail': 'Incorrect username or password'} 
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=incorrect_data)
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_users_me(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["username"] == "test_user"
    assert response.json()["email"] == "test@mail.ru"
    assert response.json()["created_at"] is not None
    assert response.json()["full_name"] is None
    assert response.json()["given_name"] is None
    assert response.json()["family_name"] is None
    assert response.json()["location"] is None
    assert response.json()["avatar"] is None


async def test_users_me_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer
