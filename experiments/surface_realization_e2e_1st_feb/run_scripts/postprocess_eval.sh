for this_set in {dev,test}
do
	# first e2e
	python ~/projects/wp_neural_pipeline/modules/postprocess_e2e.py \
		-i translate/eval_e2e_8th_march/"$this_set"*.pred.sents \
		--detok --truecase
	# then ta and e2e
	python ~/projects/wp_neural_pipeline/modules/postprocess_e2e.py \
		-i translate/eval_ta_e2e_9th_march/"$this_set"*.pred.sents \
		--detok --truecase
done

		# -r ../e2e_data_processing/stanfordnlp/8th_march_tests/"$this_set"set*mrs_for_relex.txt \
