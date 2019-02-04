#!/usr/bin/env sh
export CUDA_VISIBLE_DEVICES=0
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/1st_feb_tests/e2e_surface_realization_step_9000.pt \
	-src data/devset_eval/e2e_content_selection_step_5400.beam_5_uniq.pred.processed_for_sr.txt \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-verbose \
	-block_ngram_repeat 3 \
	-output translate/devset_eval/e2e_content_selection_step_5400.surface_realization_step_9000.beam_5_uniq.pred.processed_for_sr.final_output.txt \
	-gpu 0
