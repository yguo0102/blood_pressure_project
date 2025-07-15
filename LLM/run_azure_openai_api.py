#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
import pandas as pd
import time
from datetime import datetime, timedelta
import re
import json
import traceback
import sys


# API info
engine_id = 'gpt-35'
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"
openai.api_base = "https://sarkerlab-north-central-us.openai.azure.com/"
openai.api_key = os.getenv("OPENAI_API_KEY")

temperature = 0.5
top_p = 0.95

# prompt file
prompt_file = 'prompt/prompt.txt'
with open(prompt_file) as f:
    prompt_text = f.read()

# data file
infile = sys.argv[1] # such as train.csv
outfile = sys.argv[2]

cases = pd.read_csv(infile, dtype=str)
col_id_name = 'pmc_s'
col_text_name = 'text'
text_placeholder = '{{text}}'

#cases = cases.sample(n=1, random_state=1).reset_index(drop=True)

# keep records of answers
records = {col_id_name:[], 'response':[]}
record_file = prompt_file + '.json'
if os.path.exists(record_file):
    records_df = pd.read_json(record_file)
    for ID, res in zip(records_df[col_id_name], records_df['response']):
        records[col_id_name].append(str(ID))
        records['response'].append(res)

# Add columns to store the query processing timestamps and response token lengths
cases['full_prompt'] = None
cases['response'] = None

#############################

# Run Both Prompts
start_time = time.time()

for i in range(len(cases)):
    retry_count = 1
    max_retries = 2  # Set the maximum number of retries for a case-prompt combination

    print(f'Running {i} of {len(cases)} cases')
    while retry_count <= max_retries:
        try:
            full_prompt = prompt_text.replace(text_placeholder, cases.loc[i, col_text_name])

            # If the query has been requested, return the response
            ID = cases.loc[i, col_id_name]
            if ID in records[col_id_name]:
                if len(cases[cases[col_id_name]==ID]) == 1:
                    # If the key is not uniq, do not use the record
                    print('Recorded', ID)
                    cases.at[i, 'full_prompt'] = full_prompt
                    cases.at[i, 'response'] = records['response'][records[col_id_name].index(ID)]

            else:
                print('Call API')
                messages = [{"role":"user", 'content':full_prompt}]
                response = openai.ChatCompletion.create(
                                                        engine=engine_id,
                                                        messages=messages,
                                                        temperature=temperature,
                                                        top_p=top_p,
                                                        n=1,
                                                        stop=None)
                cases.at[i, 'full_prompt'] = full_prompt
                cases.at[i, 'response'] = response['choices'][0]['message']['content']

            print(cases.at[i, 'response'])

            break

        except Exception as e:
            traceback.print_exc()
            if isinstance(e, openai.error.InvalidRequestError):
                print(f"openai.error.InvalidRequestError: {e} at Case {i}. Skip...")
            else:
                print(f"An unexpected error occurred: {e} at Case {i}. Continuing to next case in 60s...")
                time.sleep(60)
            retry_count+=1

#######################################

# Save the cases DataFrame to a CSV file
cases.to_csv(outfile, index=False)


