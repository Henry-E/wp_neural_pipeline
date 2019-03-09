#!/usr/bin/env sh
export CUDA_VISIBLE_DEVICES=1
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/14m_sents/14m_sents_surface_realization_step_380000.pt \
	-src ../adaptive_lm_content_selection_tests_31st_jan/generate/14m/generated_temp_0.8.txt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-block_ngram_repeat 3 \
	-verbose \
	-output translate/content_selection_input/14m_sents_step_380000_with_14m_content_selection_input_temp_0.8.pred.text \
	-gpu 1
