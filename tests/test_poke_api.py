from extract.abilities import extract_abilities

def test_number_of_abilities(pikachu_sample):
    expected_number = 2
    abilities = len(extract_abilities(pikachu_sample))
    assert expected_number == abilities

def test_name_in_each_abilities(pikachu_sample):
    abilities = extract_abilities(pikachu_sample)
    assert abilities[0]['ability']['name'] == 'static'
    assert abilities[1]['ability']['name'] == 'lightning-rod'

def test_each_ability_has_hidden(pikachu_sample):
    abilities = extract_abilities(pikachu_sample)

    assert abilities[0]['is_hidden'] == False
    assert abilities[1]['is_hidden'] == True

def test_each_ability_has_slot(pikachu_sample):
    abilities = extract_abilities(pikachu_sample)

    assert abilities[0]['slot'] == 1
    assert abilities[1]['slot'] == 3

def test_each_ability_has_url(pikachu_sample):
    abilities = extract_abilities(pikachu_sample)

    assert abilities[0]['ability']['url'] == "https://pokeapi.co/api/v2/ability/9/"
    assert abilities[1]['ability']['url'] == "https://pokeapi.co/api/v2/ability/31/"

    