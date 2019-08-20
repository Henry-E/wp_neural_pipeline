#!/usr/bin/env sh
for i in {1..18}
do
	python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
		-model train/e2e_delex_8th_march_2/e2e_delex_step_"$i"000.pt \
		-src data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.surface_realization.dev.src \
		-tgt data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.surface_realization.dev.tgt \
		-report_bleu \
		-dynamic_dict \
		-share_vocab \
		-replace_unk \
		-output translate/e2e_delex_8th_march_2/e2e_delex_step_"$i"000.pred.txt \
		-log_file translate/e2e_delex_8th_march_2/e2e_delex_step_"$i"000.log.txt \
		-gpu 0
echo thiswasmodelcheckpoint"$i"
done
		# -verbose \
