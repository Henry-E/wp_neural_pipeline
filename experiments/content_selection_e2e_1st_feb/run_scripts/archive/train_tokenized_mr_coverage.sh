#!/usr/bin/env sh

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/tokenized_mr/e2e_content_selection_tok_mr \
	-save_model train/tokenized_mr_coverage/e2e_content_selection_tokenized_mr \
	--log_file train/tokenized_mr_coverage/log.txt \
	--optim adam \
	--learning_rate 0.001 \
	--encoder_type brnn \
	--layers 1 \
	--batch_size 64 \
	--word_vec_size 300 \
	--rnn_size 450 \
	--report_every 300 \
	--valid_steps 300 \
	--save_checkpoint 300 \
	--train_steps 10000 \
	`# start decaying around this point` \
	--start_decay_steps 5700 \
	--decay_steps 900 \
	--learning_rate_decay 0.25 \
	`# we\'re training with coverage now` \
	--coverage_attn \
	--gpu_ranks 0 1 \
	--world_size 2
