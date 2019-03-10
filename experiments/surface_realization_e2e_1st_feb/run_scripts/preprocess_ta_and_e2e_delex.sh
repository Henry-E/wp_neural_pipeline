#!/usr/bin/env sh

# 7th march trip advisor tests
# E2E surface realization tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/ta_e2e_delex_9th_march/ta_e2e_delex_DEEP.conllu.surface_realization.train.src \
	-train_tgt data/ta_e2e_delex_9th_march/ta_e2e_delex_DEEP.conllu.surface_realization.train.tgt \
	-valid_src data/ta_e2e_delex_9th_march/e2e_delex_DEEP.conllu.surface_realization.dev.src \
	-valid_tgt data/ta_e2e_delex_9th_march/e2e_delex_DEEP.conllu.surface_realization.dev.tgt \
	-save_data preprocess/ta_e2e_delex_9th_march/ta_e2e_delex \
	-dynamic_dict \
	-share_vocab
