awk '{print $0" , added"}' ../content_selection_e2e_1st_feb/data/e2e_delex_8th_march/e2e_delex_DEEP.conllu.content_selection.dev.src.uniq \
    | paste -d "|" - ../content_selection_e2e_1st_feb/translate/uniq_e2e_delex_8th_march/dev.e2e_delex_step_8400.pred.txt \
    | sort -R \
    | sed "s/,/, ,/g" \
    | sed G \
    | sed "s/|/\n/" \
    > manual_analysis.txt
