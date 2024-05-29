# decompyle3 version 3.9.1
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.5 (default, Sep  4 2020, 02:22:02) 
# [Clang 10.0.0 ]
# Embedded file name: /Users/gyt/projects/Blood-Pressure-Study/Codes/yuting/LLM/parse_abstract_response.py
# Compiled at: 2024-03-25 13:42:24
# Size of source mod 2**32: 4096 bytes
import pandas as pd, sys, re

def word_to_num(d):
    if " " in d:
        d1, d2 = d.split(" ")
        if re.search("^[0-9\\.]+$", d1):
            d1 = float(d1)
        else:
            return 0
        if d2 == "million":
            d = d1 * 1000000.0
        else:
            d = d1
    return d


def normalize_number(d):
    if pd.isna(d):
        return 0
    if re.search("^[0-9]*$", d):
        return int(d)
    if re.search("^[0-9\\.]* [a-zA-Z]*$", d):
        return word_to_num(d)
    return 0
    return d


def normalize_BP(d):
    mean = d
    std = "NA"
    if pd.isna(d):
        return (mean, std)
    d = d.replace("+/-", "±").replace("(", "").replace(")", "")
    if re.match("^[ 0-9±mHgNA\\.]*$", d):
        bp = re.sub("[^ 0-9±NA\\.]", "", d)
        if "±" in bp:
            (mean, std) = bp.split("±")
        else:
            print("Cannot parse:", d)
    else:
        print("Cannot parse:", d)
    return (mean, std)


def find_row_with_value(targets, data, mode, check_in_text=False):
    row_with_value = []
    for (i, row) in data.iterrows():
        if not mode == "AND":
            flag = 1
            for target in targets:
                if not pd.isna(row[target]):
                    if row[target] == "NA":
                        pass
                flag = 0
                break

            if not flag:
                row_with_value.append(i)
            if not mode == "OR":
                flag = 0
                for target in targets:
                    if not pd.isna(row[target]):
                        if re.search("[0-9]", str(row[target])):
                            flag = 1
                            break
                        if flag:
                            row_with_value.append(i)
                    return row_with_value


def parse_answer_to_varibales(targets, df):
    new_cols = {}
    for answer in df["response"]:
        for bp_var in targets:
            answer = answer + "\n"
            var_re = re.search(f"{bp_var}.*=(.+?)\n", answer)
            matched = var_re.group(1) if var_re else None
            if bp_var not in new_cols:
                new_cols[bp_var] = []
            new_cols[bp_var].append(matched)

    return new_cols


if __name__ == "__main__":
    data_file = sys.argv[1]
    out_file = sys.argv[2]
    mode = "AND"
    cols = ["pmc_s", "text_txt_en"]
    df = pd.read_csv(data_file, usecols=(cols + ["full_prompt", "response"]), dtype=str).fillna("NA")
    print("Input:", len(df))
    targets = [
     "N_male","N_female","SBP_in_male","SBP_in_female","DBP_in_male","DBP_in_female"]
    new_cols = parse_answer_to_varibales(targets, df)
    for (k, v) in new_cols.items():
        df[k] = v

    row_with_value = find_row_with_value(targets, df, mode)
    new_df = df.iloc[row_with_value].reset_index()
    print("Row with values after emtpy check: {} out of {} cases".format(len(row_with_value), len(df)))
    int_cols = [
     "N_male", "N_female"]
    new_targets = int_cols
    for col in int_cols:
        new_df[col] = new_df[col].apply(normalize_number)

    BP_cols = [
     "SBP_in_male", "SBP_in_female", "DBP_in_male", "DBP_in_female"]
    for col in BP_cols:
        parsed_output = new_df[col].apply(normalize_BP).apply(pd.Series)
        parsed_output.columns = [col + "_mean", col + "_std"]
        for column in parsed_output.columns:
            new_df.loc[:, column] = parsed_output[column]
            new_targets.append(column)

    row_with_value = find_row_with_value(new_targets, new_df, mode)
    out_df = new_df.iloc[row_with_value].reset_index()
    print("Row with values after normalization: {} out of {} cases".format(len(row_with_value), len(new_df)))
    new_df.iloc[row_with_value].to_excel(out_file, index=False, columns=(cols + new_targets))

# okay decompiling LLM/__pycache__/parse_abstract_response.cpython-38.pyc
