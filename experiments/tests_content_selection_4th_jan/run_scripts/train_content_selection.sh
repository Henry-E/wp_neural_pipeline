#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : train_content_selection
# @created     : Monday Jan 07, 2019 11:31:05 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/5th_jan_tests/1k_stories_content_selection \
	-save_model train/5th_jan_tests_brnn/1k_stories_content_selection \
	-share_embeddings \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--word_vec_size 250 \
	--valid_steps 650 \
	--save_checkpoint 1300 \
	--train_steps 8000 \
	--gpu_ranks 0 1 \
	--world_size 2
