from psycopg2 import connect

from extract.pokemons import PokeApiRequest
from extract.abilities import multiextract_pokeapi
from load import postgres_load

if __name__ == '__main__':
    # extract 100 pokemons from 1 to 100
    poke_responses = [
        PokeApiRequest('pokemon', str(i + 1)).fetch_pokeapi() for i in range(10)
    ]
    response_filter = multiextract_pokeapi(poke_responses)

    # rename order to ordering
    for data_dict in response_filter:
        data_dict['ordering'] = data_dict.pop('order')

    conn = connect(dbname="postgres", user="postgres", host="db", password="postgres")
    with conn.cursor() as cur:
        postgres_load.create_table(
            cur,
            name='pokemons',
            cols=[
                'pokeid serial PRIMARY KEY',
                'name varchar NOT NULL',
                'ordering integer NOT NULL',
            ],
        )
        postgres_load.insert_row_multiple_times(
            cur, name='pokemons', cols=['name', 'ordering'], values=response_filter
        )
        conn.commit()
    conn.close()
