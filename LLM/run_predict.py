#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
import pandas as pd
import time
from datetime import datetime, timedelta
import re
import json
import traceback

# API info
model_id = 'gpt-35'
openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = "https://yguo262.openai.azure.com/"
openai.api_key = os.getenv("OPENAI_API_KEY")
engine_id = 'gpt35'

# prompt file
prompt_file = 'prompt/abstract_p2.txt'
with open(prompt_file) as f:
    prompt_text = f.read()

# data file
cases = pd.read_csv('data/abstract_clean.csv', dtype=str)
col_id_name = 'ID'
col_text_name = 'Abstract'
text_placeholder = '{{abstract}}'

#limit to random n cases for initial testing
#cases = cases.sample(n=10, random_state=1).reset_index(drop=True)

# Add columns to store the query processing timestamps and response token lengths
cases['full_prompt'] = None
cases['response'] = None

# keep records of answers
records = {col_id_name:[], 'response':[]}
record_file = prompt_file + '.json'
if os.path.exists(record_file):
    records_df = pd.read_json(record_file)
    for ID, res in zip(records_df[col_id_name], records_df['response']):
        records[col_id_name].append(str(ID))
        records['response'].append(res)
#############################

# Run Both Prompts
start_time = time.time()

for i in range(len(cases)):
    retry_count = 1
    max_retries = 5  # Set the maximum number of retries for a case-prompt combination

    print(f'Running {i} of {len(cases)} cases')
    while retry_count <= max_retries:
        try:
            full_prompt = prompt_text.replace(text_placeholder, cases.loc[i, col_text_name])

            # If the query has been requested, return the response
            ID = cases.loc[i, col_id_name]
            if ID in records[col_id_name]:
                print('Recorded', ID)
                if type(records['response'][records[col_id_name].index(ID)]) is str:
                    cases.at[i, 'full_prompt'] = full_prompt
                    cases.at[i, 'response'] = records['response'][records[col_id_name].index(ID)]
                    continue
                else:
                    response = records['response'][records[col_id_name].index(ID)]

            else:
                print('Call API')
                messages = [{"role":"user", 'content':full_prompt}]
                response = openai.ChatCompletion.create(
                                                        engine=engine_id,
                                                        messages=messages,
                                                        temperature=0.2,
                                                        top_p=0.1,
                                                        n=1,
                                                        stop=None)
                # write new records.
                records[col_id_name].append(ID)
                records['response'].append(response)

            cases.at[i, 'full_prompt'] = full_prompt
            cases.at[i, 'response'] = response['choices'][0]['message']['content']

            print(cases.at[i, 'response'])
            if i % 100 == 0:
                with open(record_file, 'w') as f:
                    json.dump(records, f, indent = 2)

            break
        except Exception as e:
            traceback.print_exc()
            retry_count+=1
            time.sleep(60)
            print(f"An unexpected error occurred: {e} at Case {i}. Continuing to next case in 60s...")

with open(record_file, 'w') as f:
    json.dump(records, f, indent = 2)


#######################################

# Save the cases DataFrame to a CSV file
cases.to_csv(f"cases_with_responses_{model_id}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv", index=False)
print(f"Saved cases to CSV file: cases_with_responses_{model_id}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv")


