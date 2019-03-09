#!/usr/bin/env sh

# 7th march trip advisor tests
# E2E surface realization tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.surface_realization.train.src \
	-train_tgt data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.surface_realization.train.tgt \
	-valid_src data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.surface_realization.dev.src \
	-valid_tgt data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.surface_realization.dev.tgt \
	-save_data preprocess/e2e_delex_8th_march/e2e_delex \
	-dynamic_dict \
	-share_vocab 
