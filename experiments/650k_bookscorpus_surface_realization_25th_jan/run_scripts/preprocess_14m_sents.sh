#!/usr/bin/env sh

# 29th January
# Preprocess surface realization
# 14m_sents

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/14m_sents/bookscorpus.tok.ewt_ud_2.3.filter_DEEP.conllu.surface_realization.train.src \
	-train_tgt data/14m_sents/bookscorpus.tok.ewt_ud_2.3.filter_DEEP.conllu.surface_realization.train.tgt \
	-valid_src data/14m_sents/bookscorpus.tok.ewt_ud_2.3.filter_DEEP.conllu.surface_realization.dev.src \
	-valid_tgt data/14m_sents/bookscorpus.tok.ewt_ud_2.3.filter_DEEP.conllu.surface_realization.dev.tgt \
	-save_data preprocess/14m_sents/14m_sents_surface_realization \
	-dynamic_dict \
	-share_vocab \
	-src_seq_length 35 \
	-tgt_seq_length 50
