import pandas as pd
import json
import math

def split_csv_to_jsonl(input_csv, output_prefix='output', chunk_size=5000):
    # Read the large CSV file
    df = pd.read_csv(input_csv)

    # Calculate the number of chunks needed
    total_records = len(df)
    num_chunks = math.ceil(total_records / chunk_size)

    # Split the DataFrame into chunks and save each chunk as a JSONL file
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_records)

        chunk_df = df.iloc[start_idx:end_idx]
        output_file = f'{output_prefix}_{i + 1}.jsonl'

        # convert "PAT_ID": "Z4757569", "NOTE_ID": 68203404, "FULL_NOTE_TEXT_STR": to 
        # {"text": "There should be no phi in this note", "meta": {"note_id": "note_3", "patient_id": "patient_2"}, "spans": []}
        chunk_df = chunk_df.rename(columns={'FULL_NOTE_TEXT_STR':'text'})
        meta_li = []
        for _, row in chunk_df.iterrows():
            meta_li.append({'note_id':row['NOTE_ID'], 'patient_id':row['PAT_ID']})
        chunk_df.insert(0, column='meta', value=meta_li)
        chunk_df.insert(0, column='spans', value=[[] for _ in range(len(chunk_df))])

        # Convert the chunk DataFrame to a list of dictionaries and save as JSONL
        records = chunk_df.to_dict(orient='records')
        with open(output_file, 'w', encoding='utf-8') as jsonl_file:
            for record in records:
                jsonl_file.write(json.dumps(record, ensure_ascii=False) + '\n')

        print(f'Saved {output_file} with {len(records)} records.')

if __name__ == "__main__":
    input_csv_file = '/labs/samenilab/data/blood-pressure-results/BP_notes_full_text.csv'
    output_file_prefix = '/labs/samenilab/data/blood-pressure-results/BP_notes_full_text_splits/output_chunk'
    chunk_size = 5000

    split_csv_to_jsonl(input_csv_file, output_file_prefix, chunk_size)


