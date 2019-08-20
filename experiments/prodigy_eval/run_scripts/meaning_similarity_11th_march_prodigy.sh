prodigy compare meaning_similarity_11th_march \
	sents_combined/11th_march_tests/e2e_and_ta_e2e_gen.sents.jsonl \
	sents_combined/11th_march_tests/dev_set_ref.doubled.sents.jsonl \
	--diff --no-random \
	--exclude sents_combined/11th_march_tests/e2e_and_ta_e2e_gen.sents.meanining_similarity_exclude.ids \
	-F ~/projects/wp_neural_pipeline/modules/custom_compare.py
