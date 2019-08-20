#!/usr/bin/env sh
# export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/tokenized_mr/e2e_content_selection_tokenized_mr_step_8400.pt \
	-src data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src.uniq \
	-report_bleu \
	-beam_size 5 \
	-verbose \
	-output translate/tokenized_mr_coverage/e2e_content_selection_tokenized_mr_step_5400_beam_5.multiref.pred.txt \
	-log_file translate/tokenized_mr_coverage/e2e_content_selection_tokenized_mr_step_8400_beam_5.log.txt \
	-gpu 0
echo 'multireference bleu perl scores' >> translate/single_token_mr/e2e_content_selection_singletok_mr_step_5400_beam_5.log.txt
perl ~/downloads/Henry_OpenNMT-py/tools/multi-bleu.perl data/single_token_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.tgt.multiref < translate/tokenized_mr_coverage/e2e_content_selection_tokenized_mr_step_5400_beam_5.multiref.pred.txt >> translate/tokenized_mr_coverage/e2e_content_selection_tokenized_mr_step_8400_beam_5.log.txt
tail -n 5 translate/tokenized_mr_coverage/e2e_content_selection_tokenized_mr_step_8400_beam_5.log.txt
