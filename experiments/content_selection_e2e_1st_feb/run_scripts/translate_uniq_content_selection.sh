#!/usr/bin/env sh
for this_set in {dev,test}
do
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/e2e_delex_8th_march/e2e_delex_step_8400.pt \
	-src data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection."$this_set".src.uniq \
	-output translate/uniq_e2e_delex_8th_march/"$this_set".e2e_delex_step_8400.pred.txt \
	-gpu 0
done
