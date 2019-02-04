#!/usr/bin/env sh

# 14m_sents

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/1st_feb_tests/e2e_surface_realization \
	-save_model train/1st_feb_tests/e2e_surface_realization \
	--log_file train/1st_feb_tests/log.txt \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 64 \
	--word_vec_size 300 \
	--rnn_size 450 \
	--copy_attn \
	--reuse_copy_attn \
	--report_every 500 \
	--valid_steps 1000 \
	--save_checkpoint 3000 \
	--train_steps 12000 \
	--start_decay_steps 720000 \
	--gpu_ranks 0 \
	--world_size 1
