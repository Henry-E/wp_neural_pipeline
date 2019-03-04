import argparse
import os
from collections import Counter

import pyconll
from tqdm import tqdm

def accumulate_percentages(percent_in_vocab, min_percent):
    num_qualifying_sents = 0
    for percent, num_sents in percent_in_vocab.items():
        if percent > min_percent:
            num_qualifying_sents += num_sents
    return  num_qualifying_sents

def main():
    parser = argparse.ArgumentParser(description='tag, filter and create '
                                     'source')
    # parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_name', help='tripadvisor conllu'
                        ' file')
    parser.add_argument('-v', '--vocab_file_name', help='vocab from e2e')
    args = parser.parse_args()

    with open(args.vocab_file_name) as in_file:
        vocab = [line.rstrip() for line in in_file]

    trip_advisor_sents = pyconll.load.iter_from_file(args.input_file_name)

    total_num_sents = 0
    percent_in_vocab = Counter()
    for sent in trip_advisor_sents:
        total_num_tokens = 0
        num_tokens_in_vocab = 0
        for token in sent:
            this_form = token.form
            if not this_form:
                pass
            if this_form in vocab:
                num_tokens_in_vocab += 1
            total_num_tokens += 1
        try:
            this_percent_in_vocab = num_tokens_in_vocab / total_num_tokens
            this_percent_in_vocab = round(this_percent_in_vocab, 3)
        except:
            this_percent_in_vocab = 0
        percent_in_vocab[this_percent_in_vocab] += 1
        total_num_sents += 1

    print(total_num_sents)
    for this_percent in range(1, 0.5, 0.05):
        print(this_percent, accumulate_percentages(percent_in_vocab,
                                                   this_percent))


if __name__ == '__main__':
    main()
