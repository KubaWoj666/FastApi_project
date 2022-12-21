import pytest
from app import models


@pytest.fixture()
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id=test_posts[4].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[4].id, "dir": 1})
    assert response.status_code == 201


def test_vote_on_the_same_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[4].id, "dir": 1})
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[4].id, "dir": 0})
    assert response.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[4].id, "dir": 0})
    assert response.status_code == 404


def test_vote_on_post_not_exist(authorized_client,test_posts):
    response = authorized_client.post("/vote/", json={"post_id": '888888', "dir": 0})
    assert response.status_code == 404


def test_test_vote_unauthorized_user(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert response.status_code == 401
