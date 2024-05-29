import pandas as pd
from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline
from torch.utils.data import Dataset
from tqdm.auto import tqdm

# Initialize the pipeline
tokenizer = AutoTokenizer.from_pretrained("obi/deid_roberta_i2b2")
model = AutoModelForMaskedLM.from_pretrained("obi/deid_roberta_i2b2")
pipe = pipeline(task="ner", model="obi/deid_roberta_i2b2", batch_size=512, device=0)

# Read the csv data
cases = pd.read_csv('/labs/samenilab/data/blood-pressure-results/BP_notes_full_text.csv', dtype=str)
#cases = pd.read_csv('/labs/samenilab/data/blood-pressure-results/BP_notes_sample.csv', dtype=str)
#cases = cases.sample(n=512, random_state=1).reset_index(drop=True)

def data():
    for i in range(len(cases)):
        print(f'processing {i} out of {len(cases)}')
        text = cases.loc[i, 'FULL_NOTE_TEXT_STR']
        yield text


results = []
for out in pipe(data()):
    results.append(out)
cases['deid_ner_res'] = results
cases.to_csv('/labs/samenilab/data/blood-pressure-results/BP_notes_deid_output.csv', columns=['PAT_ID', 'NOTE_ID', 'deid_ner_res'], index=False)

