for this_file in db_out_files/11th_march_tests/*.accepted.ids
do
	grep -vf "$this_file" ids_combined/11th_march_tests/devset_sent_ids.both.txt \
		> "$this_file".readability.excluded_ids
done
