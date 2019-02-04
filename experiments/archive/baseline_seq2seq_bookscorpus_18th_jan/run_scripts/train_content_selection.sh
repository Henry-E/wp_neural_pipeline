#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : train_content_selection
# @created     : Monday Jan 07, 2019 11:31:05 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/7m_sents_100k_vocab/7m_sents_bookscorpus_baseline_100k_vocab \
	-save_model train/7m_sents_100k_vocab/7m_sents_bookscorpus_baseline_100k_vocab \
	--log_file train/7m_sents_100k_vocab/log.txt \
	--global_attention disabled \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 50 \
	--word_vec_size 256 \
	--rnn_size 512 \
	--max_grad_norm 2 \
	--valid_steps 20000 \
	--save_checkpoint 60000 \
	--train_steps 720000 \
	--start_decay_steps 720000 \
	--report_every 4000 \
	--gpu_ranks 0 1 \
	--world_size 2
