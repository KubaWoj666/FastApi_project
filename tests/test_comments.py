import pytest
from app import models, schemas



@pytest.fixture()
def test_comment(test_user, test_user2, test_posts, session):
    post_data = [{
        "post_id": test_posts[0].id,
        "user_id": test_user['id'],
        "comment": "comment 1"
    }, {
        "post_id": test_posts[0].id,
        "user_id": test_user2['id'],
        "comment": "comment 2"
    }]

    def create_comment_model(post):
        return models.Comments(**post)

    comment_map = map(create_comment_model, post_data)
    comment = list(comment_map)

    session.add_all(comment)
    session.commit()

    posts = session.query(models.Comments).all()
    return posts

# @pytest.fixture()
# def test_comment(test_posts, test_user, session):
#     new_comment = models.Comments(post_id=test_posts[4], user_id=test_user['id'], comment="default comment")
#     session.add(new_comment)
#     session.commit()


def test_create_comment(authorized_client, test_posts, test_user):
    response = authorized_client.post("/comment/", json={"post_id": test_posts[4].id, "user_id": test_user['id'],
                                                         "comment": "default comment"})
    new_comment = schemas.CommentOut(**response.json())
    assert response.status_code == 201
    assert new_comment.comment == "default comment"
    assert new_comment.user_id == test_user['id']


def test_the_same_user_create_another_comment_to_the_same_post(authorized_client, test_posts, test_user):
    response = authorized_client.post("/comment/", json={"post_id": test_posts[4].id, "user_id": test_user['id'],
                                                         "comment": "another comment"})
    new_comment = schemas.CommentOut(**response.json())
    assert response.status_code == 201
    assert new_comment.comment == "another comment"
    assert new_comment.user_id == test_user['id']


def test_unauthorized_user_create_comment(client, test_posts, test_user):
    response = client.post("/comment/", json={"post_id": test_posts[4].id, "user_id": test_user['id'],
                                              "comment": "default comment"})

    assert response.status_code == 401


def test_delete_comment_success(authorized_client, test_comment, test_user, test_posts):
    response = authorized_client.delete(f"/comment/{test_comment[0].comment_id}")
    assert response.status_code == 204


def test_unauthorized_user_delete_comment(client, test_comment, test_user, test_posts):
    response = client.delete(f"/comment/{test_comment[0].comment_id}")
    assert response.status_code == 401


def test_delete_comment_not_exists(authorized_client, test_comment, test_user):
    response = authorized_client.delete("/comment/888888")
    assert response.status_code == 404


def test_delete_other_user_comment(authorized_client, test_comment, test_user):
    response = authorized_client.delete(f"/comment/{test_comment[1].comment_id}")
    assert response.status_code == 403


def test_update_comment(authorized_client, test_posts, test_user, test_comment):
    data = {
        "comment_id": test_comment[0].comment_id,
        "post_id": test_posts[4].id,
        "user_id": test_user['id'],
        "comment": "update comment"
    }

    response = authorized_client.put(f"/comment/{test_comment[0].comment_id}", json=data)
    update_comment = schemas.UpdateComment(**response.json())
    assert response.status_code == 200
    assert update_comment.comment == "update comment"


def test_unauthorized_user_update_comment(client, test_comment, test_user, test_posts):
    response = client.put(f"/comment/{test_comment[0].comment_id}")
    assert response.status_code == 401


def test_update_comment_not_exists(authorized_client, test_posts, test_user, test_comment):
    data = {
        "comment_id": test_comment[0].comment_id,
        "post_id": test_posts[4].id,
        "user_id": test_user['id'],
        "comment": "update comment"
    }

    response = authorized_client.put("/comment/888888", json=data)
    assert response.status_code == 404




