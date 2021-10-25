from extract.abilities import multiextract_pokeapi


def test_number_of_results(pokelist_sample):
    expected_number = 100
    number_of_extracted_results = len(multiextract_pokeapi(pokelist_sample))
    assert expected_number == number_of_extracted_results

def test_each_result_has_abilities_name_order(pokelist_sample):
    extracted_results = multiextract_pokeapi(pokelist_sample)
    assert all(['abilities' in result for result in extracted_results])
    assert all(['name' in result for result in extracted_results])
    assert all(['order' in result for result in extracted_results])

def test_each_result_abilities_has_ability_hidden_and_slot(pokelist_sample):
    extracted_results = multiextract_pokeapi(pokelist_sample)
    for result in extracted_results:
        for ability in result.get('abilities'):
            assert 'ability' in ability
            assert 'is_hidden' in ability
            assert 'slot' in ability

def test_1st_pokemon_name_order(pokelist_sample):
    extracted_results = multiextract_pokeapi(pokelist_sample)
    assert extracted_results[0]['name'] == 'bulbasaur'
    assert extracted_results[0]['order'] == 1

def test_4th_pokemon_name_order(pokelist_sample):
    extracted_results = multiextract_pokeapi(pokelist_sample)
    assert extracted_results[3]['name'] == 'charmander'
    assert extracted_results[3]['order'] == 5

def test_1st_pokemon_ability_hidden_slot(pokelist_sample):
    extracted_results = multiextract_pokeapi(pokelist_sample)
    assert extracted_results[0]['abilities'][0]['ability']['name'] == 'overgrow'
    assert extracted_results[0]['abilities'][0]['ability']['url'] == "https://pokeapi.co/api/v2/ability/65/"
    assert extracted_results[0]['abilities'][0]['is_hidden'] == False
    assert extracted_results[0]['abilities'][0]['slot'] == 1

def test_4th_pokemon_ability_hidden_slot(pokelist_sample):
    extracted_results = multiextract_pokeapi(pokelist_sample)
    assert extracted_results[3]['abilities'][0]['ability']['name'] == 'blaze'
    assert extracted_results[3]['abilities'][0]['ability']['url'] == "https://pokeapi.co/api/v2/ability/66/"
    assert extracted_results[3]['abilities'][0]['is_hidden'] == False
    assert extracted_results[3]['abilities'][0]['slot'] == 1