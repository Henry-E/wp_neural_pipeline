#!/usr/bin/env sh
export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/1st_feb_tests/e2e_content_selection_step_5400.pt \
	-src data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src.uniq \
	-beam_size 5 \
	-verbose \
	-output translate/devset_uniq/e2e_content_selection_step_5400.beam_5_uniq.pred.txt \
	-gpu 0
