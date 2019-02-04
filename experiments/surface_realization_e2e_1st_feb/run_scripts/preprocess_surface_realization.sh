#!/usr/bin/env sh

# 1st february
# E2E surface realization tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/1st_feb_tests/trainset.utterances.ewt_ud_2.3_DEEP.conllu.surface_realization.train.src \
	-train_tgt data/1st_feb_tests/trainset.utterances.ewt_ud_2.3_DEEP.conllu.surface_realization.train.tgt \
	-valid_src data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.src \
	-valid_tgt data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.tgt \
	-save_data preprocess/1st_feb_tests/e2e_surface_realization \
	-dynamic_dict \
	-share_vocab \
