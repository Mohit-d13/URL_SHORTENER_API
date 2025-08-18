from fastapi.testclient import TestClient
import pytest
from typing import List

from app.models import User, Site


# ----------------------------------  Create shorten url link tests ---------------------------

def test_create_url(authorized_client1: TestClient):
    response = authorized_client1.post(
        '/urls/',
        json={"target_url": "https://www.google.com", "length": 6}
    )

    data = response.json()

    assert response.status_code == 201
    assert data['target_url'] == "https://www.google.com"
    assert data['url_key'] is not None

def test_create_url_unsuccessfull(authorized_client1: TestClient):
    response = authorized_client1.post(
        '/urls/',
        json={"length": 6}
    )

    assert response.status_code == 422

def test_create_url_unauthorized(client: TestClient):
    response = client.post(
        '/urls/',
        json={"target_url": "https://www.google.com", "length": 6}
    )

    assert response.status_code == 401


# ----------------------------------  Read all links tests ---------------------------


def test_read_all_sites(authorized_client1: TestClient, dummy_user1: User, sample_urls_list: List[Site]):
    response = authorized_client1.get('/urls/all/')

    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(sample_urls_list)

    for link, site in zip(data, sample_urls_list):
        assert link['target_url'] == site.target_url
        assert link['url_key'] == site.url_key
        assert link['user']['username'] == site.user.username

def test_read_all_sites_unsuccessfull(authorized_client1: TestClient):
    response = authorized_client1.get('/urls/all/')

    assert response.status_code == 404

def test_read_all_sites_unauthorized(client: TestClient):
    response = client.get('/urls/all/')

    assert response.status_code == 401


# ----------------------------------  Get a link info tests ---------------------------

def test_get_url_info(authorized_client1: TestClient, sample_url: Site):
    response = authorized_client1.get(f'/urls/info/{sample_url.url_key}/')

    data = response.json()

    assert response.status_code == 200
    assert data['target_url'] == sample_url.target_url
    assert data['url_key'] == sample_url.url_key
    assert data['user']['username'] == sample_url.user.username

def test_get_url_info_unsuccessfull(authorized_client1: TestClient):
    response = authorized_client1.get(f'/urls/info/{1}/')

    assert response.status_code == 404

def test_get_url_info_unauthorized(client: TestClient, sample_url: Site):
    response = client.get(f'/urls/info/{sample_url.url_key}/')

    assert response.status_code == 401


# ----------------------------------  Get a target link tests ---------------------------

# def test_get_target_url(client: TestClient, sample_url: Site):
#     response = client.get(f'/urls/{sample_url.url_key}/')
#     print(sample_url.url_key)

#     assert response.status_code == 307

def test_get_target_url_unsuccessfull(client: TestClient):
    response = client.get(f'/urls/{1}/')

    assert response.status_code == 404


# ----------------------------------  Delete url tests ---------------------------

def test_delete_url(authorized_client1: TestClient, sample_url: Site):
    response = authorized_client1.delete(f'/urls/{sample_url.url_key}/')

    assert response.status_code == 204

def test_delete_url_unsuccessfull(authorized_client1: TestClient):
    response = authorized_client1.delete(f'/urls/{1}/')

    assert response.status_code == 404

def test_get_url_info_unauthorized(client: TestClient, sample_url: Site):
    response = client.delete(f'/urls/{sample_url.url_key}/')

    assert response.status_code == 401





