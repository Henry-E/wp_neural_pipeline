import json
with open('db_out_files/11th_march_tests/failed_ms_ids.txt') as in_file:
    accepted_ids = [line.strip() for line in in_file]

failed_ms_lines = []
for line in open('sents_combined/11th_march_tests/gen_sents_with_intreps_for_manual_analysis.txt', encoding='utf8'):
    record = json.loads(line.split('\t')[0])
    if record['id'] in accepted_ids:
        failed_ms_lines.append(line)

with open('sents_combined/11th_march_tests/filtered_failed_meaning_similarity_lines.txt', 'w') as out_file:
    out_file.write(''.join(failed_ms_lines))
