#!/usr/bin/env sh

# 29th January
# Preprocess surface realization
# deprel

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/deprel/bookscorpus.ewt_ud_2.3.failed_18th_jan.filter_DEEP.conllu.surface_realization.train.src \
	-train_tgt data/deprel/bookscorpus.ewt_ud_2.3.failed_18th_jan.filter_DEEP.conllu.surface_realization.train.tgt \
	-valid_src data/deprel/bookscorpus.ewt_ud_2.3.failed_18th_jan.filter_DEEP.conllu.surface_realization.dev.src \
	-valid_tgt data/deprel/bookscorpus.ewt_ud_2.3.failed_18th_jan.filter_DEEP.conllu.surface_realization.dev.tgt \
	-save_data preprocess/deprel/deprel_surface_realization \
	-dynamic_dict \
	-share_vocab \
	-src_seq_length 35 \
	-tgt_seq_length 50
