#!/usr/bin/env sh
# export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/tokenized_mr/e2e_content_selection_tokenized_mr_step_8400.pt \
	-src data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src \
	-tgt data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.tgt \
	-report_bleu \
	-beam_size 5 \
	-verbose \
	-output translate/tokenized_mr_coverage/e2e_content_selection_tokenized_mr_step_8400_beam_5.pred.txt \
	-log_file translate/tokenized_mr_coverage/e2e_content_selection_tokenized_mr_step_8400_beam_5.log.txt \
	-gpu 0
