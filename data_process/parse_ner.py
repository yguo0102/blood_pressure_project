import json

res = '{"Age_precision": 0.16666666666666666, "Age_recall": 0.14285714285714285, "Age_f1": 0.15384615384615383, "Age_number": 7, "Comorbidity_precision": 0.6470588235294118, "Comorbidity_recall": 0.55, "Comorbidity_f1": 0.5945945945945946, "Comorbidity_number": 20, "DBP_precision": 0.0, "DBP_recall": 0.0, "DBP_f1": 0.0, "DBP_number": 8, "Location_precision": 0.5507246376811594, "Location_recall": 0.4367816091954023, "Location_f1": 0.48717948717948717, "Location_number": 174, "MBP_precision": 0.0, "MBP_recall": 0.0, "MBP_f1": 0.0, "MBP_number": 6, "Method_precision": 0.0, "Method_recall": 0.0, "Method_f1": 0.0, "Method_number": 6, "Race_precision": 0.0, "Race_recall": 0.0, "Race_f1": 0.0, "Race_number": 0, "SBP_precision": 0.3, "SBP_recall": 0.2, "SBP_f1": 0.24, "SBP_number": 15, "SBP_SLASH_DBP_precision": 0.0, "SBP_SLASH_DBP_recall": 0.0, "SBP_SLASH_DBP_f1": 0.0, "SBP_SLASH_DBP_number": 0, "Sex_precision": 0.9361702127659575, "Sex_recall": 0.9166666666666666, "Sex_f1": 0.9263157894736843, "Sex_number": 48, "mmHg_precision": 0.0, "mmHg_recall": 0.0, "mmHg_f1": 0.0, "mmHg_number": 2, "overall_precision": 0.5921052631578947, "overall_recall": 0.47202797202797203, "overall_f1": 0.5252918287937743, "overall_accuracy": 0.9509722453049693}'

res = json.loads(res)
print(res)

res_map = {}
for k, v in res.items():
    print(k)
    name, metric = k.split('_')
    if name not in res_map:
        res_map[name] = {}
    res_map[name][metric] = v

print(res_map)
#entity_df = {'entity':[], 'precision':[], 'recall':[], 'f1':[]}
