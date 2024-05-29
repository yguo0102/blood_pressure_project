import pandas as pd
import sys
import re
from data_utils import *

if __name__ == '__main__':

    data_file = sys.argv[1] # The output file from run_predict.py
    out_file = sys.argv[2]

    df = pd.read_csv(data_file, usecols=['pmc_s', 'text_txt_en', 'full_prompt', 'response'], dtype=str).fillna('NA')
    print('Input:', len(df))

    # Parse the text answer into a table
    #targets = [ 'bp_male_mean', 'bp_female_mean', 'bp_male_std', 'bp_female_std', 'N_male', 'N_female', 'SBP_in_male_mean', 'SBP_in_female_mean', 'SBP_in_male_std', 'SBP_in_female_std', 'DBP_in_male_mean', 'DBP_in_female_mean', 'DBP_in_male_std', 'DBP_in_female_std', ]
    targets = [ 'bp_male', 'bp_female', 'N_male', 'N_female', 'SBP_in_male_mean', 'SBP_in_female_mean', 'SBP_in_male_std', 'SBP_in_female_std', 'DBP_in_male_mean', 'DBP_in_female_mean', 'DBP_in_male_std', 'DBP_in_female_std', ]
    new_cols = parse_answer_to_varibales(targets, df)
    for k, v in new_cols.items():
        df[k] = v

    # Find the rows with all/at least one varibles predicted by the model
    row_with_value = find_row_with_value(targets, df)
    print('Row with values after emtpy check: {} out of {} cases'.format(len(row_with_value), len(df)))

    # Check the if the predicted values appear in the text
    #row_in_text = find_row_with_in_text_value([x for x in targets if x not in [ 'bp_male_mean', 'bp_female_mean', 'bp_male_std', 'bp_female_std']], 'text_txt_en', df.iloc[row_with_value])
    row_in_text = find_row_with_in_text_value([x for x in targets if x not in [ 'bp_male', 'bp_female']], 'text_txt_en', df.iloc[row_with_value])
    print('Row with in-text values: {} out of {} cases'.format(len(row_in_text), len(row_with_value)))

    # Check the bp_male and bp_female varibles
    row_male_female = find_row_with_male_female(df.iloc[row_in_text])
    print('Row with postive bp_male and bp_female values: {} out of {} cases'.format(len(row_male_female), len(row_in_text)))


    pred = []
    for i, row in df.iterrows():
        if i in row_male_female:
            pred.append(1)
        else:
            pred.append(0)
    df['pred'] = pred

    #out_df = df.iloc[row_male_female]
    out_df = df
    print(df['pmc_s'].value_counts())
    out_df.to_excel(out_file, index=False)
