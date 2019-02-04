#!/usr/bin/env sh
export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/1st_feb_tests/e2e_content_selection_step_5400.pt \
	-src data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.content_selection.dev.src \
	-tgt data/1st_feb_tests/devset.utterances.ewt_ud_2.3_DEEP.conllu.content_selection.dev.tgt \
	-report_bleu \
	-beam_size 1 \
	-random_sampling_temp 0.7 \
	-random_sampling_topk 5 \
	-verbose \
	-output translate/1st_feb_tests/e2e_content_selection_step_5400.sample.temp_0.8.top_3.pred.txt \
	-gpu 0
