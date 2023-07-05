import json

import pytest


pytestmark = pytest.mark.asyncio


async def test_create_like_or_dislike(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["user_id"] == 2
    assert response.json()["post_id"] == 1
    assert response.json()["like"] == True
    assert response.json()["dislike"] == False


async def test_create_like_or_dislike_yourself(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_like_payload = {
        "user_id": 1,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_answer = {"detail": "Can't like or dislike your post"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 400
    assert response.json() == test_answer


async def test_create_like_or_dislike_owner_id(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 3,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_answer = {"message": "user_id must be equal to the id of the current user"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 400
    assert response.json() == test_answer


async def test_create_like_or_dislike_post_not_found(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 2,
        "like": True,
        "dislike": False
    }
    test_answer = {"message": "Post cannot be Found"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 404
    assert response.json() == test_answer


async def test_create_like_or_dislike_already_exists(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_answer = {"detail": "Like or Dislike already exists"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )
    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 400
    assert response.json() == test_answer


async def test_create_like_or_dislike_both_true(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": True
    }
    test_answer = {"message": "Dislike and Like cannot be True or False at the same time"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 400
    assert response.json() == test_answer


async def test_change_like_or_dislike(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_change_data_payload = {"like": False, "dislike": True}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )
    response = await async_client.put(
        "/likes_dislikes/1", 
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["user_id"] == 2
    assert response.json()["post_id"] == 1
    assert response.json()["like"] == False
    assert response.json()["dislike"] == True


async def test_change_like_or_dislike_not_found_post(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_change_data_payload = {"like": False, "dislike": True}
    test_answer = {"message": "Post cannot be Found"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )
    response = await async_client.put(
        "/likes_dislikes/2", 
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 404
    assert response.json() == test_answer


async def test_change_like_or_dislike_not_found_like(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_change_data_payload = {"like": False, "dislike": True}
    test_answer = {"message": "Like or Dislike cannot be Found"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.put(
        "/likes_dislikes/1", 
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 404
    assert response.json() == test_answer


async def test_change_like_or_dislike_both_true(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_change_data_payload = {"like": True, "dislike": True}
    test_answer = {"message": "Dislike and Like cannot be True or False at the same time"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )
    response = await async_client.put(
        "/likes_dislikes/1", 
        content=json.dumps(test_change_data_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_like_or_dislike(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_answer = {"message": "Like or Dislike has been deleted successfully"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )
    response = await async_client.delete(
        "/likes_dislikes/1", 
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 200
    assert response.json() == test_answer


async def test_remove_like_or_dislike_not_found_post(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_like_payload = {
        "user_id": 2,
        "post_id": 1,
        "like": True,
        "dislike": False
    }
    test_answer = {"message": "Post cannot be Found"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/likes_dislikes/", 
        content=json.dumps(test_like_payload),
        headers={"Authorization": f"Bearer {token}"}    
    )
    response = await async_client.delete(
        "/likes_dislikes/2", 
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 404
    assert response.json() == test_answer


async def test_remove_like_or_dislike_not_found_like(async_client):
    test_signup_first_payload = {
        "username": "test_user", 
        "email": "test@mail.ru", 
        "password": "qwerty"
    }
    test_login_first_payload = {"username": "test_user", "password": "qwerty"}
    test_post_payload = {
        "title": "test_title",
        "content": "test_content",
        "owner_id": 1
    }
    test_signup_second_payload = {
        "username": "another_test_user", 
        "email": "another_test@mail.ru", 
        "password": "qwerty"
    }
    test_login_second_payload = {"username": "another_test_user", "password": "qwerty"}
    test_answer = {"message": "Like or Dislike cannot be Found"}

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_first_payload))
    response = await async_client.post("/users/login", data=test_login_first_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.post(
        "/posts/", 
        content=json.dumps(test_post_payload),
        headers={"Authorization": f"Bearer {token}"}
    )

    response = await async_client.post("/users/signup", content=json.dumps(test_signup_second_payload))
    response = await async_client.post("/users/login", data=test_login_second_payload)

    token = response.json()
    token = token["access_token"]

    response = await async_client.delete(
        "/likes_dislikes/1", 
        headers={"Authorization": f"Bearer {token}"}    
    )

    assert response.status_code == 404
    assert response.json() == test_answer