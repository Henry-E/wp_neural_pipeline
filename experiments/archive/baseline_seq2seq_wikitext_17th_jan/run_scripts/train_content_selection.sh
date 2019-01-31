#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : preprocess_content_selection
# @created     : Monday Jan 07, 2019 10:18:48 GMT
#
# @description : Baseline seq2seq 
######################################################################

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/3m_sents/wiki.train.tokens.detok.ewt_ud_2.3.src \
	-train_tgt data/3m_sents/wiki.train.tokens.detok.ewt_ud_2.3.tgt \
	-valid_src data/3m_sents/wiki.valid.tokens.detok.ewt_ud_2.3.src \
	-valid_tgt data/3m_sents/wiki.valid.tokens.detok.ewt_ud_2.3.tgt \
	-save_data preprocess/3m_sents/3m_sents_wkt_baseline_seq2seq \
	-shard_size 100000 \
	-dynamic_dict \
	-share_vocab \
	-src_seq_length 200 \
	-tgt_seq_length 50
