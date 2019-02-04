#!/usr/bin/env sh
export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/1st_feb_tests/e2e_surface_realization_step_9000.pt \
	-src data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.src \
	-tgt data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.surface_realization.dev.tgt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-verbose \
	-block_ngram_repeat 3 \
	-ignore_when_blocking '_(' ')_' \
	-output translate/1st_feb_tests/e2e_surface_realization_step_9000.pred.txt \
	-gpu 0
