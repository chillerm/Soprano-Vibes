import pytest
from sopranos.models.character import Character, characters, get_character_by_id, search_characters
from sopranos.utils.errors import CharacterNotFoundError

def test_character_creation():
    character = Character(1, "Tony", "Soprano")
    assert character.id == 1
    assert character.first_name == "Tony"
    assert character.last_name == "Soprano"

def test_character_to_dict():
    character = Character(1, "Tony", "Soprano")
    data = character.to_dict()
    assert data == {
        "id": 1,
        "first_name": "Tony",
        "last_name": "Soprano"
    }

def test_get_character_by_id():
    character = get_character_by_id(1)
    assert character.id == 1
    assert character.first_name == "Tony"
    assert character.last_name == "Soprano"

def test_get_character_by_id_not_found():
    with pytest.raises(CharacterNotFoundError) as exc_info:
        get_character_by_id(999)
    assert str(exc_info.value) == "Character with ID 999 not found"
    assert exc_info.value.status_code == 404

def test_search_characters_by_first_name():
    results = search_characters(first_name="Tony")
    assert len(results) > 0
    assert all("Tony" in char.first_name for char in results)

def test_search_characters_by_last_name():
    results = search_characters(last_name="Soprano")
    assert len(results) > 0
    assert all("Soprano" in char.last_name for char in results)

def test_search_characters_by_both_names():
    results = search_characters(first_name="Tony", last_name="Soprano")
    assert len(results) > 0
    assert all("Tony" in char.first_name and "Soprano" in char.last_name for char in results)

def test_search_characters_case_insensitive():
    results = search_characters(first_name="tony")
    assert len(results) > 0
    assert any("Tony" in char.first_name for char in results) 