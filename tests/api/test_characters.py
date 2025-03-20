import pytest
from sopranos import create_app
from sopranos.models.character import characters

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_get_characters(client):
    response = client.get('/api/characters/', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(characters)

def test_get_character_by_id(client):
    response = client.get('/api/characters/1/', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['first_name'] == "Tony"
    assert data['last_name'] == "Soprano"

def test_get_character_by_id_not_found(client):
    response = client.get('/api/characters/999/', follow_redirects=True)
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data
    assert 'Character with ID 999 not found' in data['message']
    assert data['status_code'] == 404

def test_search_characters_by_first_name(client):
    response = client.get('/api/characters/?firstName=Tony', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert all('Tony' in char['first_name'] for char in data)

def test_search_characters_by_last_name(client):
    response = client.get('/api/characters/?lastName=Soprano', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert all('Soprano' in char['last_name'] for char in data)

def test_search_characters_by_both_names(client):
    response = client.get('/api/characters/?firstName=Tony&lastName=Soprano', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert all('Tony' in char['first_name'] and 'Soprano' in char['last_name'] for char in data)

def test_search_characters_no_results(client):
    response = client.get('/api/characters/?firstName=NonExistent', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0

def test_invalid_input(client):
    response = client.get('/api/characters/?firstName=123', follow_redirects=True)
    assert response.status_code == 200  # Our validation allows string input
    data = response.get_json()
    assert len(data) == 0  # No characters with numeric first names

def test_search_characters_case_insensitive(client):
    response = client.get('/api/characters/?firstName=tony', follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert any('Tony' in char['first_name'] for char in data)

def test_url_redirects(client):
    """Test that URLs without trailing slashes are properly redirected"""
    response = client.get('/api/characters')
    assert response.status_code == 308  # Permanent redirect
    assert response.headers['Location'].endswith('/api/characters/') 