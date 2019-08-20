#!/usr/bin/env sh

# trip advisor tests 7th march

python /home/henrye/downloads/Henry_OpenNMT-py/train.py \
	-data preprocess/e2e_delex_8th_march/e2e_delex \
	-save_model train/e2e_delex_8th_march_3/e2e_delex \
	--log_file train/e2e_delex_8th_march_3/log.txt \
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
	--save_checkpoint 1000 \
	--train_steps 25000 \
	--decay_steps 1250 \
	--start_decay_steps 6500 \
	--gpu_ranks 0 1 \
	--world_size 2

