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
engine_id = 'gpt-35-16k'
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"
openai.api_base = "https://sarkerlab-north-central-us.openai.azure.com/"
openai.api_key = os.getenv("OPENAI_API_KEY")

temperature = 0.5
top_p = 0.95

# prompt file
prompt_file = 'prompt/p_0326.txt'
with open(prompt_file) as f:
    prompt_text = f.read()

# data file
cases = pd.read_csv('/labs/sarkerlab/yguo262/solr-9.5.0/bp_pmc_html_text_output_split_output.clean.csv', dtype=str)
col_id_name = 'pmc_s'
col_text_name = 'text_txt_en'
text_placeholder = '{{text}}'

#limit to random n cases for initial testing
selected_cases = [
'PMC3559353',
'PMC6514120',
'PMC4405040',
'PMC5753482',
'PMC10424594',
'PMC9289178',
'PMC10675948',
'PMC7093979',
'PMC10289778',
'PMC4661678',
'PMC7228482',
'PMC3559098',
'PMC10082210',
'PMC9787390',
'PMC8055644',
'PMC6322720',
'PMC6417676',
'PMC8678805',
'PMC10254090',
'PMC9519835',
]
#cases = cases.sample(n=1, random_state=1).reset_index(drop=True)
cases = cases[cases[col_id_name].isin(selected_cases)].reset_index(drop=True)


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
                                                        temperature=0.2,
                                                        top_p=0.1,
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
cases.to_csv(f"cases_with_responses_{engine_id}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv", index=False)
print(f"Saved cases to CSV file: cases_with_responses_{engine_id}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv")


