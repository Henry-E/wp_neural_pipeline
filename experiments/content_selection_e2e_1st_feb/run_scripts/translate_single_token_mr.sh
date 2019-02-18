#!/usr/bin/env sh
# export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/single_token_mr/e2e_content_selection_singletok_mr_step_5400.pt \
	-src data/single_token_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src \
	-tgt data/single_token_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.tgt \
	-report_bleu \
	-beam_size 5 \
	-verbose \
	-output translate/single_token_mr/e2e_content_selection_singletok_mr_step_5400_beam_5.pred.txt \
	-log_file translate/single_token_mr/e2e_content_selection_singletok_mr_step_5400_beam_5.log.txt \
	-gpu 0
