#!/usr/bin/env sh
for this_set in {dev,test}
do
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/ta_e2e_delex_9th_march_2/ta_e2e_delex_step_48000.pt \
	-src ../content_selection_e2e_1st_feb/translate/uniq_e2e_delex_8th_march/"$this_set".e2e_delex_step_8400.pred.sents \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-output translate/eval_ta_e2e_9th_march/"$this_set".ta_e2e_step_48000.pred.sents \
	-gpu 0
echo thiswasmodelcheckpoint"$i"
done
	# -verbose \
