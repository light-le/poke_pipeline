import csv
import os
from load.csv_load import CSVLoader, read_csv_data, write_csv_data
from mockito import when, verify, mock

def test_if_pokemons_csv_has_some_names(pokelist_sample):
    CSVLoader(pokelist_sample).load_poke_data_to_csv()
    poke_name_orders = read_csv_data('pokemons.csv', 'name', 'order')
    with open('pokemons.csv') as pokecsv:
        pokedata = csv.DictReader(pokecsv)
        pokenames = [row['name'] for row in pokedata]
    for expected_name_order in [['bulbasaur', '1'],
                                ['charmander', '5'],
                                ['squirtle', '10'],
                                ['pikachu', '35']]:
        assert expected_name_order in poke_name_orders
    os.remove('pokemons.csv')

def test_if_pokemons_csv_has_unique_id_and_name(pokelist_sample):
    CSVLoader(pokelist_sample).load_poke_data_to_csv()
    pokenames = read_csv_data('pokemons.csv', 'name')
    pokeids = read_csv_data('pokemons.csv', 'pokeid')

    assert len(pokenames) == len(set(pokenames))
    assert len(pokeids) == len(set(pokeids))
    os.remove('pokemons.csv')


def test_if_abilities_csv_has_some_names_urls(pokelist_sample):
    CSVLoader(pokelist_sample).load_abilities_data_to_csv()
    ability_name_urls = read_csv_data('abilities.csv', 'name', 'url')
    for expected_name_url in [['overgrow', "https://pokeapi.co/api/v2/ability/65/"],
                              ['chlorophyll', "https://pokeapi.co/api/v2/ability/34/"],
                              ['blaze', "https://pokeapi.co/api/v2/ability/66/"],
                              ['solar-power', "https://pokeapi.co/api/v2/ability/94/"]]:
        assert expected_name_url in ability_name_urls
    os.remove('abilities.csv')

def test_if_all_ability_data_are_unique(pokelist_sample):
    CSVLoader(pokelist_sample).load_abilities_data_to_csv()
    ability_id = read_csv_data('abilities.csv', 'abilityid')
    ability_name = read_csv_data('abilities.csv', 'name')
    ability_url = read_csv_data('abilities.csv', 'url')

    assert len(ability_id) == len(set(ability_id))
    assert len(ability_name) == len(set(ability_name))
    assert len(ability_url) == len(set(ability_url))
    os.remove('abilities.csv')

def test_write_csv_data():
    dummywriter = mock()
    with when(csv).writer(...).thenReturn(dummywriter):
        with when(dummywriter).writerow(...):
            with when(dummywriter).writerows(...):
                write_csv_data('csvname', [['row1'], ['row2']], 'col')
                
                verify(dummywriter).writerow(['col'])
                verify(dummywriter).writerows([['row1'], ['row2']])
    os.remove('csvname')


def test_if_pokemons_csv_has_header_id_name_order(pokelist_sample):
    CSVLoader(pokelist_sample).load_poke_data_to_csv()
    with open('pokemons.csv') as pokecsv:
        pokedata = csv.reader(pokecsv)
        for line in pokedata:
            assert line == ['pokeid', 'name', 'order']
            break
    os.remove('pokemons.csv')
    

def test_if_abilities_csv_has_header_id_name_url(pokelist_sample):
    CSVLoader(pokelist_sample).load_abilities_data_to_csv()
    with open('abilities.csv') as abilitycsv:
        abilitydata = csv.reader(abilitycsv)
        for line in abilitydata:
            assert line == ['abilityid', 'name', 'url']
            break
    os.remove('abilities.csv')