#!/usr/bin/env sh

# 6th february
# E2E content selection tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/single_token_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.train.src \
	-train_tgt data/single_token_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.train.tgt \
	-valid_src data/single_token_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src \
	-valid_tgt data/single_token_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.tgt \
	-save_data preprocess/single_token_mr/e2e_content_selection_singletok_mr \
