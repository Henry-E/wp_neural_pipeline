#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : preprocess_content_selection
# @created     : Monday Jan 07, 2019 10:18:48 GMT
#
# @description : Baseline seq2seq 
######################################################################

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/7m_sents/bookscorpus.tok.7m_sents.train.ewt_ud_2.3.src \
	-train_tgt data/7m_sents/bookscorpus.tok.7m_sents.train.ewt_ud_2.3.tgt \
	-valid_src data/7m_sents/bookscorpus.tok.7m_sents.valid.ewt_ud_2.3.src \
	-valid_tgt data/7m_sents/bookscorpus.tok.7m_sents.valid.ewt_ud_2.3.tgt \
	-save_data preprocess/7m_sents_100k_vocab/7m_sents_bookscorpus_baseline_100k_vocab \
	-shard_size 100000 \
	-dynamic_dict \
	-share_vocab \
	-src_seq_length 200 \
	-tgt_seq_length 50 \
	-src_vocab_size 100000 \
	-tgt_vocab_size 100000

