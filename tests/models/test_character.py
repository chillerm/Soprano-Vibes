import pytest
from sopranos.models.character import Character, get_character_by_id, search_characters

def test_character_creation():
    character = Character(1, "Tony", "Soprano")
    assert character.id == 1
    assert character.first_name == "Tony"
    assert character.last_name == "Soprano"

def test_character_to_dict():
    character = Character(1, "Tony", "Soprano")
    char_dict = character.to_dict()
    assert char_dict == {
        "id": 1,
        "first_name": "Tony",
        "last_name": "Soprano"
    }

def test_get_character_by_id():
    character = get_character_by_id(1)
    assert character is not None
    assert character.first_name == "Tony"
    assert character.last_name == "Soprano"

def test_get_character_by_id_not_found():
    character = get_character_by_id(999)
    assert character is None

def test_search_characters_by_first_name():
    results = search_characters(first_name="Tony")
    assert len(results) == 1
    assert results[0].first_name == "Tony"

def test_search_characters_by_last_name():
    results = search_characters(last_name="Soprano")
    assert len(results) == 5  # All Soprano family members

def test_search_characters_by_both_names():
    results = search_characters(first_name="Tony", last_name="Soprano")
    assert len(results) == 1
    assert results[0].first_name == "Tony"
    assert results[0].last_name == "Soprano"

def test_search_characters_case_insensitive():
    results = search_characters(first_name="tony")
    assert len(results) == 1
    assert results[0].first_name == "Tony" 