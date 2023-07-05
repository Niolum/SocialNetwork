import json

import pytest


pytestmark = pytest.mark.asyncio


async def test_create_post(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "test_title"
    assert response.json()["content"] == "test_content"
    assert response.json()["owner_id"] == 1
    assert response.json()["created_at"] is not None
    assert response,json()["owner"] is not None


async def test_create_post_title_exists(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_answer = {"message": "There is already a Post with this title"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_create_post_owner_id(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 2
    }
    test_answer = {"message": "owner_id must be equal to the id of the current user"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_create_post_incorrect(async_client):
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 2
    }
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_get_post(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.get(
        "/posts/1", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "test_title"
    assert response.json()["content"] == "test_content"
    assert response.json()["owner_id"] == 1
    assert response.json()["created_at"] is not None
    assert response,json()["owner"] is not None


async def test_get_post_not_found(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_answer = {"message": "Post cannot be Found"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.get(
        "/posts/2", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_get_posts(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.get(
        "/posts/", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["title"] == "test_title"
    assert response.json()[0]["content"] == "test_content"
    assert response.json()[0]["owner_id"] == 1
    assert response.json()[0]["created_at"] is not None
    assert response,json()[0]["owner"] is not None


async def test_change_post(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_change_data_payload = {
        "title": "another_test_title",
        "content": "another_test_content",
        "owner_id": 1
    }
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.put(
        "/posts/1",
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "another_test_title"
    assert response.json()["content"] == "another_test_content"
    assert response.json()["owner_id"] == 1
    assert response.json()["created_at"] is not None
    assert response,json()["owner"] is not None


async def test_change_post_owner_user_exception(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_change_data_payload = {
        "title": "another_test_title",
        "content": "another_test_content",
        "owner_id": 2
    }
    test_answer = {"message": "owner_id must be equal to the id of the current user"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.put(
        "/posts/1",
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_change_post_owner_user_exception(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_change_data_payload = {
        "title": "another_test_title",
        "content": "another_test_content",
        "owner_id": 1
    }
    test_answer = {"message": "The post must be owned by the current user"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.put(
        "/posts/2",
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_change_post_title_exists(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_change_data_payload = {
        "title": "test_title",
        "content": "another_test_content",
        "owner_id": 1
    }
    test_answer = {"message": "There is already a Post with this title"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.put(
        "/posts/1",
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_change_post_incorrect(async_client):
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.put(
        "/posts/1", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_remove_post(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_answer = {"message": "Post has been deleted successfully"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.delete(
        "/posts/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_remove_post_owner_user_exception(async_client):
    test_signup_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_request_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_answer = {"message": "The post must be owned by the current user"}
    response = await async_client.post("/users/signup", content=json.dumps(test_signup_payload))
    response = await async_client.post("/users/login", data=test_login_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_request_payload),
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await async_client.delete(
        "/posts/2",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_post_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.delete(
        "/posts/1", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json() == test_answer