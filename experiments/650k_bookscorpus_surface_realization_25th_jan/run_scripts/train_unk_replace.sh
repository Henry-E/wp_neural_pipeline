#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @created     : Monday Jan 07, 2019 11:31:05 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/unk_replace/unk_replace_surface_realization \
	-save_model train/unk_replace/unk_replace_surface_realization \
	--log_file train/unk_replace/log.txt \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 64 \
	--word_vec_size 300 \
	--rnn_size 450 \
	--copy_attn \
	--reuse_copy_attn \
	--report_every 1000 \
	--valid_steps 2000 \
	--save_checkpoint 20000 \
	--train_steps 40000 \
	--start_decay_steps 720000 \
	--gpu_ranks 0 1 \
	--world_size 2
