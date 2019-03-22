python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/e2e_delex_8th_march/e2e_delex_step_8400.pt \
	-src data/e2e_delex_8th_march/testset_mrs.delex.tok.uniq \
	-output translate/uniq_e2e_delex_8th_march/testset_mrs.delex.tok.uniq.pred.txt \
	-gpu 0
