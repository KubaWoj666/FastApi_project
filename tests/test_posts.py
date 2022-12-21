from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts")
    def validate(post):
        return schemas.PostsOut(**post)
    post_map = map(validate, response.json())
    #print(list(post_map))
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/88888")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostsOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published",[
    ("super title", "super content", True),
    ("bed title", "bed content", False),
    ("3 title", "3 content", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    create_post = schemas.PostOut(**response.json())
    assert response.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user['id']


def test_create_post_default_published_false(authorized_client, test_posts, test_user,):
    response = authorized_client.post("/posts/", json={"title": "default title", "content": "default content"})
    create_post = schemas.PostOut(**response.json())
    assert response.status_code == 201
    assert create_post.title == "default title"
    assert create_post.content == "default content"
    assert create_post.published == False
    assert create_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_posts):
    response = client.post("/posts/", json={"title": "default title", "content": "default content"})
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts, test_user):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_post_success(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_post_no_exist(authorized_client, test_posts, test_user):
    response = authorized_client.delete("/posts/88888")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/{test_posts[4].id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[0].id
    }

    response = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    update_post = schemas.PostCreate(**response.json())
    assert response.status_code == 200
    assert update_post.title == data['title']
    assert update_post.content == data['content']


def test_unauthorized_user_update_post(client, test_posts, test_user):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    response = authorized_client.put("/posts/8000000", json=data)

    assert response.status_code == 404


