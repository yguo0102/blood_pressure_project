import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import json
import sys

import time
from datetime import datetime, timedelta

model_path = sys.argv[1] # model name in Huggingface
data_file = sys.argv[2]
out_file = sys.argv[3]

# prompt file
prompt_file = 'prompt/p_0326.txt'
with open(prompt_file) as f:
    prompt_text = f.read()

# data file
cases = pd.read_csv(data_file, dtype=str)
col_id_name = 'pmc_s'
col_text_name = 'text'
text_placeholder = '{{text}}'

#limit to random n cases for initial testing
# cases = cases.sample(n=10, random_state=1).reset_index(drop=True)

# Add columns to store the query processing timestamps and response token lengths
cases['full_prompt'] = None
cases['response'] = None

# Run Both Prompts
start_time = time.time()

# Initialize the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")

for i in range(len(cases)):

    print(f'Running {i} of {len(cases)} cases')
    full_prompt = prompt_text.replace(text_placeholder, cases.loc[i, col_text_name])
    message = {'role':'user', 'content': full_prompt}

    # Re-format the prompt
    prompt = tokenizer.apply_chat_template([message], tokenize=False)
    print(prompt)

    inputs = tokenizer(prompt, return_tensors='pt', truncation=True).to(model.device)
    tokens = model.generate(
        **inputs,
        max_new_tokens=500,
        temperature=0.5,
        top_p=0.95,
    )
    output = tokenizer.batch_decode(tokens[:, inputs.input_ids.shape[-1]:], skip_special_tokens=False)[0]
    print(output)

    cases.at[i, 'full_prompt'] = full_prompt
    cases.at[i, 'response'] = output
    print(cases.at[i, 'response'])

#######################################

# Save the cases DataFrame to a CSV file
cases.to_csv(out_file, index=False)
print(f"Saved cases to CSV file: {out_file}")


