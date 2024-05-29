import pandas as pd
import glob

files = glob.glob('/labs/sarkerlab/yguo262/biomedical_data/pma/manuscript_2024/*.sec.csv')
data = []
for f in files:
    data.append(pd.read_csv(f, dtype=str))
out = pd.concat(data, ignore_index=True)
out.to_csv('sections.csv', index=False)
