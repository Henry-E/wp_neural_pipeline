#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : train_content_selection
# @created     : Monday Jan 07, 2019 11:31:05 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/3m_sents/3m_sents_wkt_baseline_seq2seq \
	-save_model train/3m_sents/3m_sents_wkt_baseline_seq2seq \
	--global_attention disabled \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--word_vec_size 200 \
	--rnn_size 300 \
	--valid_steps 350 \
	--save_checkpoint 2800 \
	--train_steps 140000 \
	--report_every 175 \
	--gpu_ranks 0 1 \
	--world_size 2
