import argparse
import os
import csv
import re
from collections import Counter

import stanfordnlp
from tqdm import tqdm

def get_name_and_near(mr):
    # neither might be present
    xname = ''
    xnear = ''
    for act in mr:
        act_type = act[0:act.find('[')].strip()
        value = act[act.find('[')+1:act.find(']')]
        if act_type == 'name':
            xname = value.strip().replace(' ', '\s+')
        elif act_type == 'near':
            xnear = value.strip().replace(' ', '\s+')
            # this one specifically has a lot of misspellings
            if value == 'Crowne Plaza Hotel':
                xnear += '|Crown\\s+Plaza\\s+Hotel'
    return xname, xnear

def delexicalize_utterance(mr, utt):
    name, near = get_name_and_near(mr.strip().split(', '))
    # we allow multiple spaces between words and ignore case
    if name:
        out_utt = re.sub(name, 'Xname', utt, flags=re.IGNORECASE)
    if near:
        out_utt = re.sub(near, 'Xnear', out_utt, flags=re.IGNORECASE)

    # We find that with the sentence tokenization it helps to lower case the
    # international names. We don't have to use a dict but this is how we had
    # it in a different file
    international_things = {'Chinese':'chinese', 'Japanese':'japanese',
                            'French':'french', 'Indian':'indian',
                            'English':'english', 'Italian':'italian'}
    for word, lowercase_word in international_things.items():
        out_utt = out_utt.replace(word, lowercase_word)

    # TODO then finally do manual substitution for things we know are missed by
    # the simple regexes. But we will wait until manually inspecting the output
    # before writing these. Just to confirm our initial analysis
    return out_utt

def main():
    parser = argparse.ArgumentParser(description='parse e2e with stanfordnlp'
                                     'and output many files later steps')
    parser.add_argument('-i', '--input_file_names', nargs='*',
                        help='e2e csv files; train,dev,test')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    args = parser.parse_args()

    nlp = stanfordnlp.Pipeline()
    # output_file_name = os.path.join(args.output_dir_name,
    #                                 'trip_advisor_full_corpus.conllu')
    for input_file_name in args.input_file_names:
        e2e_lines = csv.reader(open(input_file_name))
        # skip the header
        next(e2e_lines)
        e2e_conllu = []
        tok_sents = []
        # add header, will be output to csv
        mr_and_tok_utts = ['mr,ref']
        # Now we need some other output variables that were in the delex module
        multi_ref_count = Counter()
        mrs_for_relex = []
        sent_ids = []
        print(os.path.basename(input_file_name))
        for mr, utt in tqdm(e2e_lines):
            multi_ref_count[mr] += 1
            multi_ref_id = multi_ref_count[mr]
            # do delex on the utterances
            delex_utt = delexicalize_utterance(mr, utt)
            parsed_utt = nlp(delex_utt)
            this_conllu = parsed_utt.conll_file.conll_as_string()
            e2e_conllu.append(this_conllu)
            this_utt_sents = []
            for i, sent in enumerate(parsed_utt.sentences):
                tok_sent = ' '.join([word.text for word in sent.words])
                tok_sents.append(tok_sent)
                this_utt_sents.append(tok_sent)
                mrs_for_relex.append(mr)
                sent_ids.append('_'.join([mr.replace(' ', ''),
                                          str(multi_ref_id),
                                          str(i)]))
            tok_utt = ' _sent_ '.join(this_utt_sents)
            mr_and_tok_utts.append(','.join(['"' + mr + '"', '"' + tok_utt + '"']))
        # write to file
        input_file_root = \
            os.path.basename(os.path.splitext(input_file_name)[0])

        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '.conllu')
        with open(output_file_name, 'w') as out_file:
            # the conllu strings have new lines between them already
            out_file.write(''.join(e2e_conllu))
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '.delex.sents.tok')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(tok_sents))
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '.tok.csv')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(mr_and_tok_utts))
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '_mrs_for_relex.txt')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(mrs_for_relex))
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '_sent_ids.txt')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(sent_ids))

if __name__ == '__main__':
    main()
