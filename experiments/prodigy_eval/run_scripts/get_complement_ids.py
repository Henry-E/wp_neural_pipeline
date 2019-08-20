with open('db_out_files/11th_march_tests/missing_readability_ids.txt') as in_file:
    accepted_ids = [line.strip() for line in in_file]

with open('ids_combined/11th_march_tests/devset_sent_ids.both.txt') as in_file:
    complement_of_accepted_ids = []
    for this_id in in_file:
        if this_id.strip() in accepted_ids:
            continue
        complement_of_accepted_ids.append(this_id.strip())

with open('db_out_files/11th_march_tests/final_set_of_excluded_ids_49_left.ids', 'w') as out_file:
    out_file.write('\n'.join(complement_of_accepted_ids))
