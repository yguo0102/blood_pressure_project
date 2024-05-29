import sqlite3
import pandas as pd

data_file = '/labs/sarkerlab/yguo262/biomedical_data/pma/manuscript_2024/sections.csv'
db_file = '/labs/sarkerlab/yguo262/biomedical_data/pma/manuscript_2024/sections.db'

df = pd.read_csv(data_file, dtype=str)
r, c = df.shape
print(f"The data has {r} row and {c} columns")


# create sqlite database into local memory (RAM)
db = sqlite3.connect(db_file)
cur = db.cursor()
cur.execute('create virtual table manuscript using fts5(pmc, text_id, text, tokenize="porter unicode61");')
# bulk index records
cur.executemany('insert into manuscript (pmc, text_id, text) values (?,?,?);', df[['pmc', 'text_id', 'text']].to_records(index=False))
db.commit()
print('Create', db_file)
