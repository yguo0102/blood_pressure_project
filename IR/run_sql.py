import sqlite3
import pandas as pd

db_file = '/labs/sarkerlab/yguo262/biomedical_data/pma/manuscript_2024/par.db'
db = sqlite3.connect(db_file)
cur = db.cursor()
