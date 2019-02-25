#!/usr/bin/env sh

# 14m_sents

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/22nd_feb_tests/e2e_surface_realization \
	-save_model train/25th_feb_tests/e2e_surface_realization \
	--log_file train/25th_feb_tests/log.txt \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 64 \
	--word_vec_size 300 \
	--rnn_size 450 \
	--share_embeddings \
	--copy_attn \
	--reuse_copy_attn \
	--report_every 500 \
	--valid_steps 500 \
	--save_checkpoint 500 \
	--train_steps 12000 \
	--start_decay_steps 6000 \
	--decay_steps 2000 \
	--gpu_ranks 0 1 \
	--world_size 2
