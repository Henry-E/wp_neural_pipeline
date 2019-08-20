for this_set in {dev,test}
do
cat translate/uniq_e2e_delex_8th_march/"$this_set".e2e_delex_step_8400.pred.txt | \
	sed 's/$/\nbreak/ ; s/ new_sent /\n/g' > \
	translate/uniq_e2e_delex_8th_march/"$this_set".e2e_delex_step_8400.pred.sents
done
