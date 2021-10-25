import csv
from extract.abilities import multiextract_pokeapi

class CSVLoader:
    def __init__(self, pokelist) -> None:
        self.pokelist = pokelist
        self.pokedicts = multiextract_pokeapi(pokelist)

    def load_poke_data_to_csv(self):
        poke_flat_name_order = [[id, pokedict.get('name'), pokedict.get('order')] for id, pokedict in enumerate(self.pokedicts)]
        write_csv_data('pokemons.csv', poke_flat_name_order, 'pokeid', 'name', 'order')

    def load_abilities_data_to_csv(self):
        pokeabilities = [pokedict.get('abilities') for pokedict in self.pokedicts]
        abilities = set()
        for pokeability in pokeabilities:
            for ability in pokeability:
                abilities.add((ability.get('ability').get('name'), ability.get('ability').get('url')))
        abilities_list = [[id, name, url] for id, (name, url) in enumerate(abilities)]
        write_csv_data('abilities.csv', abilities_list, 'abilityid', 'name', 'url')

def write_csv_data(csvname, data, *fieldnames):
    with open(csvname, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(list(fieldnames))
        csvwriter.writerows(data)

def read_csv_data(csvname: str, *cols) -> list:
    with open(csvname, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        cols = csvreader.fieldnames if not cols else cols
        if len(cols) == 1:
            [col] = cols
            return [row[col] for row in csvreader]
        return [[row[col] for col in cols] for row in csvreader]