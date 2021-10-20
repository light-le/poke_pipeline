def extract_abilities(sample):
    sample_abilities = sample.get("abilities", {})
    return [extract_ability(abi) for abi in sample_abilities]

def extract_ability(abi):
    ability = {
        'ability': {
            'name': abi.get('ability').get('name'),
            'url': abi.get('ability').get('url'),
        },
        'is_hidden': abi.get('is_hidden'),
        'slot': abi.get('slot'),
    }
    return ability

def multiextract_pokeapi(pokelist):
    return [extract_abilities_name_order(poke) for poke in pokelist]

def extract_abilities_name_order(poke):
    return {
        'abilities': [extract_ability_ishidden_slot(ability) for ability in poke.get('abilities')],
        'name': poke.get('name'),
        'order': poke.get('order'),
    }

def extract_ability_ishidden_slot(ability):
    return {
        'ability': {
            'name': ability.get('ability').get('name'),
            'url': ability.get('ability').get('url'),
            },
        'is_hidden': ability.get('is_hidden'),
        'slot': ability.get('slot'), 
    }