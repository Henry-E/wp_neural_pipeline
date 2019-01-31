#!/usr/bin/env sh
export CUDA_VISIBLE_DEVICES=1
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/14m_sents/14m_sents_surface_realization_step_380000.pt \
	-src data/14m_sents/bookscorpus.tok.ewt_ud_2.3.filter_DEEP.conllu.surface_realization.dev.src \
	-tgt data/14m_sents/bookscorpus.tok.ewt_ud_2.3.filter_DEEP.conllu.surface_realization.dev.tgt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-block_ngram_repeat 3 \
	-output translate/14m_sents/14m_sents_step_380000.pred.txt \
	-log_file translate/14m_sents/14m_sents_step_380000.log.txt \
	-gpu 1
