from mockito import verify, mock
from functools import reduce
from load.postgres_load import create_table, insert_multiple_rows, insert_row_multiple_times


def mock_cur():
    return mock({"execute": lambda x, y=[]: None})

def test_create_table():
    cur = mock_cur()
    create_table(cur, name='pokemons', cols=['pokeid SERIAL PRIMARY KEY', 'name VARCHAR(50) NOT NULL', 'order INTEGER NOT NULL'])
    verify(cur, times=1).execute('CREATE TABLE IF NOT EXISTS pokemons (pokeid SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, order INTEGER NOT NULL)')

data = [
    {'name': 'haunter', 'order': 139},
    {'name': 'pidgey', 'order': 21},
    {'name': 'pikachu', 'order': 35},
]

def test_insert_row_multiple_times():
    cur = mock_cur()
    insert_row_multiple_times(cur, name='pokemons', cols=['name', 'order'], values=data)
    verify(cur, times=1).execute('INSERT INTO pokemons (name, order) VALUES (%s, %s)', ['haunter', '139'])
    verify(cur, times=1).execute('INSERT INTO pokemons (name, order) VALUES (%s, %s)', ['pidgey', '21'])
    verify(cur, times=1).execute('INSERT INTO pokemons (name, order) VALUES (%s, %s)', ['pikachu', '35'])


def test_insert_multiple_rows():
    cur = mock_cur()

    insert_multiple_rows(cur, name='pokemons', cols=['name', 'order'], values=data)
    verify(cur, times=1).execute("INSERT INTO pokemons (name, order) VALUES (%s, %s), (%s, %s), (%s, %s)", 
                                 ['haunter', '139', 'pidgey', '21', 'pikachu', '35'])