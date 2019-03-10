#!/usr/bin/env sh
for i in {42..66..3};
do
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/ta_e2e_delex_9th_march_2/ta_e2e_delex_step_"$i"000.pt \
	-src data/ta_e2e_delex_9th_march/e2e_delex_DEEP.conllu.surface_realization.dev.src \
	-tgt data/ta_e2e_delex_9th_march/e2e_delex_DEEP.conllu.surface_realization.dev.tgt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-output translate/ta_e2e_delex_9th_march_2/ta_e2e_delex_step_"$i"000.pred.txt \
	-log_file translate/ta_e2e_delex_9th_march_2/ta_e2e_delex_step_"$i"000.log.txt \
	-gpu 0
echo thiswasmodelcheckpoint"$i"
done
	# -verbose \
