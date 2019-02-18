#!/usr/bin/env sh
export CUDA_VISIBLE_DEVICES=1
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/deprel/deprel_surface_realization_step_40000.pt \
	-src data/deprel/head_2000_train.src \
	-tgt data/deprel/head_2000_train.tgt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-block_ngram_repeat 3 \
	-output translate/deprel/head_2000_train_step_40000.pred.txt \
	-log_file translate/deprel/head_2000_train_step_40000.log.txt \
	-gpu 1
