#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : preprocess_surface_realization
# @created     : Monday Jan 07, 2019 10:38:21 GMT
#
# @description :
######################################################################

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/16th_jan_tests/wiki.train.tokens.100k.ewt_ud_2.3_DEEP.surface_realization.src \
	-train_tgt data/16th_jan_tests/wiki.train.tokens.100k.ewt_ud_2.3_DEEP.surface_realization.tgt \
	-valid_src data/16th_jan_tests/wiki.valid.tokens.100k.ewt_ud_2.3_DEEP.surface_realization.src \
	-valid_tgt data/16th_jan_tests/wiki.valid.tokens.100k.ewt_ud_2.3_DEEP.surface_realization.tgt \
	-save_data preprocess/16th_jan_tests/100k_surface_realization \
	-dynamic_dict \
	-share_vocab \
	-src_seq_length 35 \
	-tgt_seq_length 65

