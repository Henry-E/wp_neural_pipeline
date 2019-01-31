#!/usr/bin/env sh

# 14m_sents

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/14m_sents/14m_sents_surface_realization \
	-save_model train/14m_sents/14m_sents_surface_realization \
	--log_file train/14m_sents/log.txt \
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
	--train_steps 600000 \
	--start_decay_steps 720000 \
	--gpu_ranks 0 1 \
	--world_size 2
