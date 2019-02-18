export CUDA_VISIBLE_DEVICES=1
python /home/henrye/downloads/Henry_OpenNMT-py/translate.py \
	-model train/unk_replace/unk_replace_surface_realization_step_20000.pt \
	-src data/unk_replace/bookscorpus.ewt_ud_2.3.failed_18th_jan.filter_DEEP.conllu.surface_realization.dev.src \
	-tgt data/unk_replace/bookscorpus.ewt_ud_2.3.failed_18th_jan.filter_DEEP.conllu.surface_realization.dev.tgt \
	-report_bleu \
	-dynamic_dict \
	-share_vocab \
	-replace_unk \
	-block_ngram_repeat 3 \
	-output translate/unk_replace/unk_replace_surface_realization_step_20000.pred.txt \
	-log_file translate/unk_replace/unk_replace_surface_realization_step_20000.log.txt \
	-gpu 1
