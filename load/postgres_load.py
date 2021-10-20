from functools import reduce

def create_table(cur, name, cols):
    cur.execute(f'CREATE TABLE IF NOT EXISTS {name} ({", ".join(cols)})')

def insert_row_multiple_times(cur, name, cols, values):
    for datadict in values:
        rowdata = [str(datadict[col]) for col in cols]
        cur.execute(f"INSERT INTO {name} ({', '.join(cols)}) VALUES ({', '.join(['%s']*len(cols))})", rowdata)

def insert_multiple_rows(cur, name, cols, values):
    rowdata = [[str(data[col]) for col in cols] for data in values]
    flatten_row = reduce((lambda a,b: a+b), rowdata)
    cur.execute(f"INSERT INTO {name} ({', '.join(cols)}) VALUES {', '.join(['('+', '.join(['%s']*len(cols))+')']*len(values))}",
                flatten_row)
