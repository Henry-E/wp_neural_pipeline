sed 's/$/_ta/' data/11th_march_tests/devset_sent_ids.txt > ids_combined/11th_march_tests/devset_sent_ids.txt.ta_e2e
sed 's/$/_e2e/' data/11th_march_tests/devset_sent_ids.txt > ids_combined/11th_march_tests/devset_sent_ids.txt.e2e
# We use awk because it adds new lines between files
awk 1 ids_combined/11th_march_tests/devset_sent_ids.txt.e2e ids_combined/11th_march_tests/devset_sent_ids.txt.ta_e2e > ids_combined/11th_march_tests/devset_sent_ids.both.txt
