import pytest
from flask import url_for

def test_get_all_characters(client):
    response = client.get('/api/characters/', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 10  # Total number of characters

def test_get_character_by_id(client):
    response = client.get('/api/characters/1/', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert data['first_name'] == "Tony"
    assert data['last_name'] == "Soprano"

def test_get_character_by_id_not_found(client):
    response = client.get('/api/characters/999/', follow_redirects=True)
    assert response.status_code == 404

def test_search_characters_by_first_name(client):
    response = client.get('/api/characters/?firstName=Tony', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['first_name'] == "Tony"

def test_search_characters_by_last_name(client):
    response = client.get('/api/characters/?lastName=Soprano', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 5  # All Soprano family members

def test_search_characters_by_both_names(client):
    response = client.get('/api/characters/?firstName=Tony&lastName=Soprano', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['first_name'] == "Tony"
    assert data[0]['last_name'] == "Soprano"

def test_search_characters_case_insensitive(client):
    response = client.get('/api/characters/?firstName=tony', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['first_name'] == "Tony"

def test_url_redirects(client):
    """Test that URLs without trailing slashes are properly redirected"""
    response = client.get('/api/characters')
    assert response.status_code == 308  # Permanent redirect
    assert response.headers['Location'].endswith('/api/characters/') 