#!/usr/bin/env sh

######################################################################
# @author      : henrye (henrye@boole01.cluster)
# @file        : preprocess_content_selection
# @created     : Monday Jan 07, 2019 10:18:48 GMT
#
# @description : Content selection (where does this boilerplate come from)
######################################################################

python ~/downloads/Henry_OpenNMT-py/preprocess.py \
	-train_src data/5th_jan_tests/valid.tok.txt.ud.special_DEEP.train.src \
	-train_tgt data/5th_jan_tests/valid.tok.txt.ud.special_DEEP.train.tgt \
	-valid_src data/5th_jan_tests/valid.tok.txt.ud.special_DEEP.dev.src \
	-valid_tgt data/5th_jan_tests/valid.tok.txt.ud.special_DEEP.dev.tgt \
	-save_data preprocess/5th_jan_tests/1k_stories_content_selection \
	-dynamic_dict \
	-share_vocab \
	-src_seq_length 1002 \
	-tgt_seq_length 35
