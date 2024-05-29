import pandas as pd
import re
import json

log_file = 'run.log'
cases = pd.read_csv('/labs/sarkerlab/yguo262/solr-9.5.0/bp_pmc_html_result_split_output.csv', dtype=str)
prompt_file = 'prompt/p_0324.txt'
record_file = prompt_file + '.json'

col_id_name = 'pmc_s'
col_text_name = 'text_pieces_txt_en'

with open(log_file) as f:
    text = f.read()

records = {col_id_name:[], col_text_name:[]}

for i, row in cases.iterrows():
    print(f'Processing {i} of {len(cases)}')
    case_id = row[col_id_name]

    x = re.search(f'Running {i} of {len(cases)} cases\nCall API\n(.*)Running {i+1} of {len(cases)} cases', text, re.DOTALL)
    if x and 'An unexpected error occurred' not in x.group(1):
        records[col_id_name].append(case_id)
        records[col_text_name].append(x.group(1))

with open(record_file, 'w') as f:
    json.dump(records, f, indent = 2)

