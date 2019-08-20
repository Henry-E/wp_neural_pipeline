#!/usr/bin/env sh
for i in {12..108..12}
do
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/e2e_delex_8th_march/e2e_delex_step_"$i"00.pt \
	-src data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection.dev.src \
	-tgt data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection.dev.tgt \
	-report_bleu \
	-output translate/e2e_delex_8th_march/e2e_delex_step_"$i"00.pred.txt \
	-gpu 0
echo thisstepis"$i"
done

# 	-random_sampling_temp 0.7 \
# 	-random_sampling_topk 5 \
