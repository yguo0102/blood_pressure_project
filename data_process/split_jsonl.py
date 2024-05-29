from sklearn.model_selection import train_test_split

lines = []
with open('/labs/samenilab/data/blood-pressure-results/BP_notes_full_text_uniq.jsonl', 'r') as f:
    for line in f:
        lines.append(line)

print(len(lines))
train, test = train_test_split(lines, test_size=0.05)

with open('/labs/samenilab/data/blood-pressure-results/BP_notes_full_text_uniq.train.jsonl', 'w') as f:
    for line in train:
        f.write(line)

with open('/labs/samenilab/data/blood-pressure-results/BP_notes_full_text_uniq.test.jsonl', 'w') as f:
    for line in test:
        f.write(line)
print('train:{}, test:{}'.format(len(train), len(test)))
