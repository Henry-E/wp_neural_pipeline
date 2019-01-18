import argparse
import os
import re
from collections import deque
import pyconll
from tqdm import tqdm

def get_ud_sent_tokens(sentence):
    tokens = []
    for token in sentence:
        if token.form:
            tokens.append(token.form)
        else:
            # it seemingly mistakes underscores for None objects
            tokens.append('_')
    return tokens

def main():
    parser = argparse.ArgumentParser(description='create source and target')
    parser.add_argument('--input_file_names', '-i', nargs='*',
                        help='udpipe input file')
    parser.add_argument('--output_dir_name', '-o', help='experiment data dir')
    args = parser.parse_args()

    for input_file_name in args.input_file_names:
        with open(input_file_name) as in_file:
            udpipe_input = in_file.read().replace('# newdoc\n', '')
        sections = udpipe_input.split('# newpar')

        baseline_seq2seq_src = []
        baseline_seq2seq_tgt = []

        # we read it's much quicker to join a list of strings than keep a
        # continuously updating string https://waymoot.org/home/python_string/
        for section in tqdm(sections):
            this_section = pyconll.load.iter_from_string(section)
            # keeping a rolling context with max length of src + tgt of 200
            context_sents = deque()
            num_context_sents_toks = 0
            for sent in this_section:
                ud_sent_tokens = get_ud_sent_tokens(sent)
                num_ud_sent_toks = len(ud_sent_tokens)
                if num_context_sents_toks + num_ud_sent_toks > 200:
                    # remove sentences until total tokens is under 200
                    while True:
                        if 'new_sent' not in context_sents:
                            # it's possible 1 sent + 1 tgt is > 200
                            # And we don't really want this so we reset the
                            # context and ignore this source target pair
                            context_sents = deque()
                            num_context_sents_toks = 0
                            print(num_context_sents_toks, num_ud_sent_toks)
                            break
                        cur_token = context_sents.popleft()
                        num_context_sents_toks -= 1
                        if cur_token == 'new_sent' and \
                           num_context_sents_toks + num_ud_sent_toks <= 200:
                            break
                # We limit generation to 50 tokens max, this accounts for
                # about 5% of sentences
                if context_sents and num_ud_sent_toks <= 50:
                    baseline_seq2seq_src.append(' '.join(context_sents))
                    baseline_seq2seq_tgt.append(' '.join(ud_sent_tokens))
                if context_sents:
                    context_sents.extend(['new_sent'] + ud_sent_tokens)
                    num_context_sents_toks += 1 + num_ud_sent_toks
                else:
                    context_sents.extend(ud_sent_tokens)
                    num_context_sents_toks += num_ud_sent_toks

        input_file_root = \
            os.path.basename(os.path.splitext(input_file_name)[0])
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root +
                                        '.src')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(baseline_seq2seq_src))
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root +
                                        '.tgt')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(baseline_seq2seq_tgt))

if __name__ == '__main__':
    main()
