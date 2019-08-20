#!/usr/bin/env sh

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/e2e_delex_8th_march/e2e_delex \
	-save_model train/e2e_delex_8th_march/e2e_delex \
	--log_file train/e2e_delex_8th_march/log.txt \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 64 \
	--word_vec_size 300 \
	--rnn_size 450 \
	--report_every 150 \
	--valid_steps 300 \
	--save_checkpoint 1200 \
	--train_steps 14000 \
	--start_decay_steps 4500 \
	--decay_steps 900 \
	--gpu_ranks 0 1 \
	--world_size 2
