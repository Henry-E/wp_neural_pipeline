#!/usr/bin/env sh
# export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/tokenized_mr/e2e_content_selection_tok_mr_step_5400.pt \
	-src data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src.uniq \
	-beam_size 5 \
	-verbose \
	-output translate/tokenized_mr/e2e_content_selection_tok_mr_step_5400_beam_5.pred.txt \
	-log_file translate/tokenized_mr/e2e_content_selection_tok_mr_step_5400_beam_5.log.txt \
	-gpu 0
echo 'multireference bleu perl scores' >> translate/tokenized_mr/e2e_content_selection_tok_mr_step_5400_beam_5.log.txt
perl ~/downloads/Henry_OpenNMT-py/tools/multi-bleu.perl data/tokenized_mr/e2e_delex-text.txt.ewt_ud_2.3_DEEP.conllu.content_selection.dev.tgt.multiref < translate/tokenized_mr/e2e_content_selection_tok_mr_step_5400_beam_5.pred.txt >> translate/tokenized_mr/e2e_content_selection_tok_mr_step_5400_beam_5.log.txt
tail -n 5 translate/tokenized_mr/e2e_content_selection_tok_mr_step_5400_beam_5.log.txt
