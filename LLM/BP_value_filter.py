import pandas as pd

df = pd.read_csv('data/abstract_pma24.csv', dtype=str)
print('data size', len(df))

out = df[df['abstract'].str.contains('mmHg') | df['abstract'].str.contains('mm Hg')]
print('result:', len(out))

out.to_csv('data/abstract_pma24_mmhg.csv', index=False)
