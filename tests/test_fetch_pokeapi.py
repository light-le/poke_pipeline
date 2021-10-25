# url = https://pokeapi.co/api/v2/

import requests
import pytest
from mockito import when, verify, mock

from extract.pokemons import PokeApiRequest, PokeApiError



def test_fetch_pokemon_pikachu():
    with when(requests).get(...):
        PokeApiRequest('pokemon', 'pikachu').make_request()
        verify(requests, times=1).get('https://pokeapi.co/api/v2/pokemon/pikachu')

def test_fetch_ability_static():
    with when(requests).get(...):
        PokeApiRequest('ability', 'static').make_request()
        verify(requests, times=1).get('https://pokeapi.co/api/v2/ability/static')

def test_fetch_pokeapi_return_a_dict():
    ok_response = mock({"status_code": 200, "text": '{"a": "dict"}'})
    with when(requests).get(...).thenReturn(ok_response):
        poke = fetch_with_dummy_pokeapi_request_object()
        assert poke == {'a': 'dict'}

def fetch_with_dummy_pokeapi_request_object():
    return PokeApiRequest('info', 'name').fetch_pokeapi()

OK_RESPONSE = mock({"status_code": 200, "text": '{"valid": "response"}'})

def test_fetching_pokeapi_error_if_error_response():
    for error_status_code in [400, 401, 403, 500, 501, 502, 503]:
        error_response = mock({"status_code": error_status_code})
        with pytest.raises(PokeApiError) as error:
            with when(requests).get(...).thenReturn(error_response).thenReturn(error_response):
                fetch_with_dummy_pokeapi_request_object()
        assert error.value.args[0] == f'{error_status_code} Bad Request'

        with when(requests).get(...).thenReturn(error_response).thenReturn(OK_RESPONSE):
            valid_response = fetch_with_dummy_pokeapi_request_object()
            assert valid_response == {'valid': 'response'}

def test_fetching_pokeapi_error_if_empty_response():
    for empty_body in ["", None]:
        empty_response = mock({'status_code': 200, 'text': empty_body})
        with pytest.raises(PokeApiError) as error:
            with when(requests).get(...).thenReturn(empty_response):
                fetch_with_dummy_pokeapi_request_object()
        assert error.value.args[0] == 'Empty Response'

def test_fetching_pokeapi_error_if_invalid_json():
    invalid_response = mock({"status_code": 200, "text": '{not json}'})
    with pytest.raises(PokeApiError) as error:
        with when(requests).get(...).thenReturn(invalid_response):
            response = fetch_with_dummy_pokeapi_request_object()
    assert error.value.args[0] == "Invalid JSON"

def test_multirequests_all_ok_response():
    with when(requests).get(...).thenReturn(OK_RESPONSE):
        for i in range(100):
            response = fetch_with_dummy_pokeapi_request_object()
            assert response == {'valid': 'response'}