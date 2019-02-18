#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @created     : Monday Jan 07, 2019 11:31:05 GMT
#
# @description :
######################################################################

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/linearized/linearized_surface_realization \
	-save_model train/linearized_transformer/linearized_transformer_surface_realization \
	--log_file train/linearized_transformer/log.txt \
	-layers 6 \
	-copy_attn \
       	-rnn_size 512 \
	-word_vec_size 512 \
	-transformer_ff 2048 \
	-heads 8 \
	-encoder_type transformer \
	-decoder_type transformer \
	-position_encoding \
	-max_generator_batches 2 \
	-dropout 0.1 \
	-batch_type tokens \
	-normalization tokens \
	-accum_count 2 \
	-optim adam \
	-adam_beta2 0.998 \
	-decay_method noam \
	-warmup_steps 40000 \
	-learning_rate 2 \
	-max_grad_norm 0 \
	-param_init 0  \
	-param_init_glorot \
	-label_smoothing 0.1 \
	--batch_size 64 \
	--report_every 500 \
	--valid_steps 2000 \
	--save_checkpoint 20000 \
	--train_steps 200000 \
	--gpu_ranks 0 1 \
	--world_size 2
