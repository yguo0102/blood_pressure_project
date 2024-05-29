import pandas as pd

df = pd.read_csv('../LLM/data/abstract_pma21.csv', dtype=str)
out = df.sample(n=int(len(df)*0.01), random_state=1)
print('size', len(out))
out.to_csv('../LLM/data/abstract_pma21_sample.csv', index=False)
