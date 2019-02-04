#!/usr/bin/env sh

# 1st february
# E2E content selection tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/1st_feb_tests/trainset.utterances.ewt_ud_2.3_DEEP.conllu.content_selection.train.src \
	-train_tgt data/1st_feb_tests/trainset.utterances.ewt_ud_2.3_DEEP.conllu.content_selection.train.tgt \
	-valid_src data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src \
	-valid_tgt data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.content_selection.dev.tgt \
	-save_data preprocess/1st_feb_tests/e2e_content_selection \
