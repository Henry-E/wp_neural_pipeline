for this_file in db_out_files/11th_march_tests/*.jsonl
do
sed -n 's/{"id":"\(.*\)","input".*"answer":"accept"}/\1/p' "$this_file" > "$this_file".accepted.ids
done
