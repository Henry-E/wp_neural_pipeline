#!/usr/bin/env sh
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/ta_100percent_7th_march/[insert file here] \
	-src data/ta_100percent_7th_march/e2e_DEEP.conllu.surface_realization.dev.src \
	-tgt data/ta_100percent_7th_march/e2e_DEEP.conllu.surface_realization.dev.tgt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-verbose \
	-output translate/ta_100percent_7th_march/e2e_surface_realization_step_11000.pred.txt \
	-log_file translate/ta_100percent_7th_march/e2e_surface_realization_step_11000.log.txt \
	-gpu 0
