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
openai.api_base = "https://sarkerlab-north-central-us.openai.azure.com/"
openai.api_key = os.getenv("OPENAI_API_KEY")
engine_id = 'gpt-35'

# data file
cases = pd.read_csv('data/output_abstract24_p2_parsed_selected.csv', dtype=str)
col_id_name = 'doi'

#limit to random n cases for initial testing
cases = cases.sample(n=5, random_state=5).reset_index(drop=True)

# Set repeating query
repeat_prompt = "Are you sure? Do it again and give a score ranging from 1 to 5 how confident you are for the answer."
n_repeat = 3
for k in range(n_repeat):
    cases[f'response_{k}'] = None

#############################

# Run Both Prompts
start_time = time.time()

for i in range(len(cases)):
    for k in range(n_repeat):
        retry_count = 1
        max_retries = 5  # Set the maximum number of retries for a case-prompt combination

        print(f'Running {i} of {len(cases)} cases')
        while retry_count <= max_retries:
            try:
                print('Call API')
                messages = [
                            {"role":"user", 'content':cases.loc[i, 'full_prompt']},
                            {"role":"assistant", "content": cases.at[i, 'response']},
                            {"role":"user", 'content':repeat_prompt}
                ]

                for j in range(k-1):
                    messages.append({"role":"assistant", "content": cases.at[i, f'response_{j}']})
                    messages.append({"role":"user", 'content':repeat_prompt})

                print(messages)
                response = openai.ChatCompletion.create(
                                                        engine=engine_id,
                                                        messages=messages,
                                                        temperature=0.2,
                                                        top_p=0.1,
                                                        n=1,
                                                        stop=None)

                cases.at[i, f'response_{k}'] = response['choices'][0]['message']['content']

                print(cases.at[i, f'response_{k}'])
                break
            except Exception as e:
                traceback.print_exc()
                retry_count+=1
                time.sleep(60)
                print(f"An unexpected error occurred: {e} at Case {i}. Continuing to next case in 60s...")


#######################################

# Save the cases DataFrame to a CSV file
cases.to_csv(f"cases_with_responses_{model_id}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv", index=False)
print(f"Saved cases to CSV file: cases_with_responses_{model_id}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv")


