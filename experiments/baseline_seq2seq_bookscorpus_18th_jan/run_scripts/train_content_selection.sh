#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : train_content_selection
# @created     : Monday Jan 07, 2019 11:31:05 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/7m_sents/7m_sents_bookscorpus_baseline_seq2seq \
	-save_model train/7m_sents_really_long_training/7m_sents_bookscorpus_baseline_seq2seq \
	--log_file train/7m_sents_really_long_training/log.txt \
	--global_attention disabled \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 100 \
	--word_vec_size 128 \
	--rnn_size 512 \
	--max_grad_norm 2 \
	--valid_steps 10000 \
	--save_checkpoint 30000 \
	--train_steps 360000 \
	--report_every 2000 \
	--gpu_ranks 0 1 \
	--world_size 2
