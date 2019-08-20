import json
for line in open('db_out_files/11th_march_tests/meaning_similarity_11th_march.jsonl', encoding='utf8'):
    record = json.loads(line)
    if record['answer'] == 'reject':
        print(record['id'])
