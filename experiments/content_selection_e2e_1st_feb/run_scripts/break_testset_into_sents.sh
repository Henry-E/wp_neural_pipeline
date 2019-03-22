cat translate/uniq_e2e_delex_8th_march/testset_mrs.delex.tok.uniq.pred.txt | \
	sed 's/$/\nbreak/ ; s/ new_sent /\n/g' > \
	translate/uniq_e2e_delex_8th_march/testset_mrs.delex.tok.uniq.pred.sents
