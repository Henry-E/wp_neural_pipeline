#!/usr/bin/env sh

# 1st february
# E2E surface realization tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.surface_realization.train.src \
	-train_tgt data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.surface_realization.train.tgt \
	-valid_src data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.src \
	-valid_tgt data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.tgt \
	-save_data preprocess/tokenized_mr/e2e_surface_realization_tokenized_mr \
	-dynamic_dict \
	-share_vocab \
