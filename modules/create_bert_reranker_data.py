import argparse
import os
import random
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(description='''take in tokenized mr and
                                    target utterances, then output a tsv of
                                    them for use in a bert reranker ''')
    parser.add_argument('--input_mr_file_name', help='tokenized mr file name')
    parser.add_argument('--input_utt_file_name', help='utterance file name')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-n', '--num_dataset_repeats',
                        type=int, default=1,
                        help='''artificially increase size of dataset by
                        repeating''')
    args = parser.parse_args()

    with open(args.input_mr_file_name) as in_file:
        source_mrs = [line.rstrip() for line in in_file]
    with open(args.input_utt_file_name) as in_file:
        target_utterances = [line.rstrip() for line in in_file if line.rstrip()]

    multiref_lookup = defaultdict(list)

    correct_lines = []
    for src, tgt in zip(source_mrs, target_utterances):
        correct_lines.append('\t'.join(['correct', src, tgt]))
        multiref_lookup[src].append(tgt)

    out_lines = []
    for _ in range(args.num_dataset_repeats):
        out_lines.extend(correct_lines)
        # for src in source_mrs:
        #     while True:
        #         different_src = random.choice(source_mrs)
        #         if different_src == src:
        #             continue
        #         tgt = random.choice(multiref_lookup[different_src])
        #         break
        #     out_lines.append('\t'.join(['wrong', src, tgt]))

    input_file_ext = args.input_mr_file_name.split('.')[-2]
    output_file_name = os.path.join(args.output_dir_name,
                                    'bert_reranking.repeats_' +
                                    str(args.num_dataset_repeats) + '.' +
                                    input_file_ext)
    with open(output_file_name, 'w') as out_file:
        out_file.write('\n'.join(out_lines))

if __name__ == '__main__':
    main()
