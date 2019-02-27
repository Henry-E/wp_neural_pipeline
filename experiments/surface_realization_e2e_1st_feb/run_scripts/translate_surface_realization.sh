#!/usr/bin/env sh
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/25th_feb_tests_2/e2e_surface_realization_step_11000.pt \
	-src data/22nd_feb_tests/e2e_delex_sents.txt.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.src \
	-tgt data/22nd_feb_tests/e2e_delex_sents.txt.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.tgt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-verbose \
	-output translate/25th_feb_tests/e2e_surface_realization_step_11000.pred.txt \
	-log_file translate/25th_feb_tests/e2e_surface_realization_step_11000.log.txt \
	-gpu 0
