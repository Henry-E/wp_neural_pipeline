import json
from collections import Counter
with open('db_out_files/11th_march_tests/meaning_similarity_11th_march.jsonl.accepted.ids') as in_file:
    accepted_ids = [this.strip() for this in in_file]

ids_seen = Counter()
all_annotated_ids = []
for line in open('db_out_files/11th_march_tests/readability_11th_march.jsonl', encoding='utf8'):
    record = json.loads(line)
    if record['id'] in accepted_ids:
        ids_seen['yes'] += 1
    else:
        ids_seen['no'] += 1
    ids_seen[record['id']] += 1
    all_annotated_ids.append(record['id'])
# for key, value in ids_seen.items():
#     if value > 3:
#         print(key, value)
for this_id in accepted_ids:
    if this_id not in all_annotated_ids:
        print(this_id)

