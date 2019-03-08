#!/usr/bin/env sh

# 7th march trip advisor tests
# E2E surface realization tests

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/ta_100percent_7th_march/tripadvisor_min_1.0_percent_overlap_DEEP.conllu.surface_realization.train.src \
	-train_tgt data/ta_100percent_7th_march/tripadvisor_min_1.0_percent_overlap_DEEP.conllu.surface_realization.train.tgt \
	-valid_src data/ta_100percent_7th_march/e2e_DEEP.conllu.surface_realization.dev.src \
	-valid_tgt data/ta_100percent_7th_march/e2e_DEEP.conllu.surface_realization.dev.tgt \
	-save_data preprocess/ta_100percent_7th_march/e2e_surf_rel \
	-dynamic_dict \
	-share_vocab 
