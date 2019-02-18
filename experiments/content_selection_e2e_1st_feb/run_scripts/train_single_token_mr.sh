#!/usr/bin/env sh

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/single_token_mr/e2e_content_selection_singletok_mr \
	-save_model train/single_token_mr/e2e_content_selection_singletok_mr \
	--log_file train/single_token_mr/e2e_content_selection_singletok.log.txt \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 64 \
	--word_vec_size 300 \
	--rnn_size 450 \
	--report_every 300 \
	--valid_steps 600 \
	--save_checkpoint 1800 \
	--train_steps 10000 \
	--start_decay_steps 720000 \
	--gpu_ranks 0 1 \
	--world_size 2
