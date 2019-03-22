#!/usr/bin/env sh

# 1st february
# E2E content selection tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection.train.src \
	-train_tgt data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection.train.tgt \
	-valid_src data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection.dev.src \
	-valid_tgt data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection.dev.tgt \
	-save_data preprocess/e2e_delex_8th_march/e2e_delex \
