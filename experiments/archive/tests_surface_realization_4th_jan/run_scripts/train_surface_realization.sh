#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : train_surface_realization
# @created     : Monday Jan 07, 2019 11:31:27 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/5th_jan_tests/1k_stories_surface_realization \
	-save_model train/5th_jan_tests_one_layer/1k_stories_surface_realization \
	-share_embeddings \
	--optim adam \
	--learning_rate 0.001 \
	--layers 1 \
	--word_vec_size 250 \
	--valid_steps 390 \
	--save_checkpoint 780 \
	--train_steps 4700 \
	--gpu_ranks 0 1 \
	--world_size 2
