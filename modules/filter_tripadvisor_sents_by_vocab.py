import argparse
import os
from collections import Counter

import pyconll
from tqdm import tqdm
import numpy

def accumulate_percentages(percent_in_vocab, min_percent):
    num_qualifying_sents = 0
    for percent, num_sents in percent_in_vocab.items():
        if min_percent <= percent:
            num_qualifying_sents += num_sents
    return  num_qualifying_sents

def main():
    parser = argparse.ArgumentParser(description='tag, filter and create '
                                     'source')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_name', help='tripadvisor conllu'
                        ' file')
    parser.add_argument('-v', '--vocab_file_name', help='vocab from e2e')
    args = parser.parse_args()

    with open(args.vocab_file_name) as in_file:
        vocab = [line.rstrip() for line in in_file]

    trip_advisor_sents = pyconll.load.iter_from_file(args.input_file_name)

    total_num_sents = 0
    all_sents_percent_in_vocab = []
    percent_in_vocab = Counter()
    for sent in trip_advisor_sents:
        total_num_tokens = 0
        num_tokens_in_vocab = 0
        for token in sent:
            this_form = token.form
            if not this_form:
                pass
            # making sure to lower case form since vocab is all lower case
            if this_form.lower() in vocab:
                num_tokens_in_vocab += 1
            total_num_tokens += 1
        try:
            this_percent_in_vocab = num_tokens_in_vocab / total_num_tokens
            this_percent_in_vocab = round(this_percent_in_vocab, 3)
        except:
            this_percent_in_vocab = 0
        percent_in_vocab[this_percent_in_vocab] += 1
        all_sents_percent_in_vocab.append(this_percent_in_vocab)
        total_num_sents += 1

    print(total_num_sents)
    print('\t'.join(['min %', 'total', 'as a %']))
    for min_percent in numpy.arange(1, 0.5, -0.05):
        this_many_sents = accumulate_percentages(percent_in_vocab, min_percent)
        print('\t'.join(str(x) for x in [round(min_percent, 2),
                                         this_many_sents,
                                         round(this_many_sents / total_num_sents, 2)]))

    # let's see how slow this is first before trying to optimize
    for min_percent in numpy.arange(1, 0.5, -0.05):
        trip_advisor_sents = pyconll.load.iter_from_file(args.input_file_name)
        out_conllu = []
        for this_percent, sent in tqdm(zip(all_sents_percent_in_vocab,
                                           trip_advisor_sents),
                                       total=total_num_sents):
            if min_percent <= this_percent:
                out_conllu.append(sent.conll())
        input_file_root = \
            os.path.basename(os.path.splitext(args.input_file_name)[0])
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root +
                        '_min_{}_percent_overlap.conllu'.format(min_percent))
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(out_conllu))

if __name__ == '__main__':
    main()
