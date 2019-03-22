# using awk to print because it correctly puts new lines between files
awk 1 data/11th_march_tests/e2e_delex_step_8000.pred.txt.pp.relex.deunk.detok.tc \
	data/11th_march_tests/ta_e2e_delex_step_48000.pred.txt.pp.relex.deunk.detok.tc \
	> \
	sents_combined/11th_march_tests/e2e_and_ta_e2e_gen.sents
awk 1 data/11th_march_tests/devset.delex.sents.tok.pp.relex.detok \
	data/11th_march_tests/devset.delex.sents.tok.pp.relex.detok \
	> \
	sents_combined/11th_march_tests/dev_set_ref.doubled.sents
