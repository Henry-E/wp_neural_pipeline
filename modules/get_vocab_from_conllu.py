import argparse
import os
from collections import Counter
import pyconll
from pyconll.tree import SentenceTree
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='''run through all the words in
                                     a conllu file and get a vocabulary based
                                     on min numbers of occurences''')
    parser.add_argument('-i', '--input_file_name', help='a train conllu file')
    parser.add_argument('-o', '--output_dir_name', help='output dir for vocab')
    parser.add_argument('--min_num_occurrences', default=10, type=int,
                        help='''the minimum number of times a word must appear
                                in the corpus to be part of the vocab file''')
    args = parser.parse_args()

    conllu_sents = pyconll.load.iter_from_file(args.input_file_name)
    all_the_words = Counter()
    for sent in tqdm(conllu_sents):
        for token in sent:
            if token.form:
                all_the_words[token.form] += 1
    vocab_out = []
    # only take words which appear min_num_occurences times
    for word, num_occurences in tqdm(all_the_words.most_common()):
        if num_occurences < args.min_num_occurrences:
            break
        vocab_out.append(word)

    input_file_root = \
        os.path.basename(os.path.splitext(args.input_file_name)[0])
    output_file_name = os.path.join(args.output_dir_name,
                                    input_file_root + '.vocab.txt')
    with open(output_file_name, 'w') as out_file:
        out_file.write('\n'.join(vocab_out))

if __name__ == '__main__':
    main()
