#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : train_content_selection
# @created     : Monday Jan 07, 2019 11:31:05 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/16th_jan_tests/100k_wkt_content_selection \
	-save_model train/16th_jan_tests_very_small/100k_wkt_content_selection \
	--global_attention disabled \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--word_vec_size 200 \
	--rnn_size 300 \
	--valid_steps 350 \
	--save_checkpoint 350 \
	--train_steps 8500 \
	--report_every 200 \
	--gpu_ranks 0 1 \
	--world_size 2
