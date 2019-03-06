import argparse
import os
import csv

import stanfordnlp
from tqdm import tqdm

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
        print(os.path.basename(input_file_name))
        for mr, utt in tqdm(e2e_lines):
            parsed_utt = nlp(utt)
            this_conllu = parsed_utt.conll_file.conll_as_string()
            e2e_conllu.append(this_conllu)
            this_utt_sents = []
            for sent in parsed_utt.sentences:
                tok_sent = ' '.join([word.text for word in sent.words])
                tok_sents.append(tok_sent)
                this_utt_sents.append(tok_sent)
            tok_utt = '_sent_'.join(this_utt_sents)
            mr_and_tok_utts.append(','.join([mr, tok_utt]))
        # write to file
        input_file_root = \
            os.path.basename(os.path.splitext(input_file_name)[0])

        output_file_name = os.path.join(args.output_file_name,
                                        input_file_root + '.conllu')
        with open(output_file_name, 'w') as out_file:
            # the conllu strings have new lines between them already
            out_file.write(''.join(e2e_conllu))
        output_file_name = os.path.join(args.output_file_name,
                                        input_file_root + '.sents.tok')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(tok_sents))
        output_file_name = os.path.join(args.output_file_name,
                                        input_file_root + '.tok.csv')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(mr_and_tok_utts))

if __name__ == '__main__':
    main()
