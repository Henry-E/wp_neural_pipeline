#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : preprocess_content_selection
# @created     : Monday Jan 07, 2019 10:18:48 GMT
#
# @description : Content selection (where does this boilerplate come from)
######################################################################

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/16th_jan_tests/wiki.train.tokens.100k.ewt_ud_2.3_DEEP.content_selection.src \
	-train_tgt data/16th_jan_tests/wiki.train.tokens.100k.ewt_ud_2.3_DEEP.content_selection.tgt \
	-valid_src data/16th_jan_tests/wiki.valid.tokens.100k.ewt_ud_2.3_DEEP.content_selection.src \
	-valid_tgt data/16th_jan_tests/wiki.valid.tokens.100k.ewt_ud_2.3_DEEP.content_selection.tgt \
	-save_data preprocess/16th_jan_tests/100k_wkt_content_selection \
	-dynamic_dict \
	-share_vocab \
	-src_seq_length 200 \
	-tgt_seq_length 35
