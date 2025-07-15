import pandas as pd, sys, re

def find_row_with_value(targets, data):
    row_with_value = []
    for i, row in data.iterrows():
        flag = 1
        for target in targets:
            if row[target] == "NA":
                flag = 0
                break

        if flag:
            row_with_value.append(i)
    return row_with_value


def find_row_with_in_text_value(targets, text_col, df):
    row_in_text = []
    for (i, row) in df.iterrows():
        flag = 1
        for col in targets:
            value = row[col]
            if str(value) not in row[text_col]:
                flag = 0
                break
        if flag:
            row_in_text.append(i)
    return row_in_text


def find_row_with_male_female(df):
    row_male_female = []
    for (i, row) in df.iterrows():
        if int(row["bp_male_mean"]) == 1 and int(row["bp_female_mean"]) == 1 and \
           int(row["bp_male_std"]) == 1 and int(row["bp_female_std"]) == 1:
            row_male_female.append(i)
    return row_male_female


def parse_answer_to_varibales(targets, df):
    new_cols = {}
    for answer in df["response"]:
        for bp_var in targets:
            answer = answer + "\n"
            var_re = re.search(f"{bp_var}.*=([0-9\\.]+)", answer)
            matched = var_re.group(1) if var_re else None
            if bp_var not in new_cols:
                new_cols[bp_var] = []
            if matched:
                new_cols[bp_var].append(matched)
            else:
                new_cols[bp_var].append(0)

    return new_cols

# okay decompiling LLM/__pycache__/data_utils.cpython-38.pyc
