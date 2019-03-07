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
    parser.add_argument('-i', '--input_file_names', nargs='*',
                        help='trainset conllu files')
    parser.add_argument('-o', '--output_dir_name', help='output dir for vocab')
    parser.add_argument('--min_num_occurrences', default=10, type=int,
                        help='the minimum number of times a word must appear'
                        ' in the corpus to be part of the vocab file')
    parser.add_argument('--max_vocab_size', default=50000, type=int,
                        help='max vocab allowed, this is the usual size,'
                        'however it will be a little larger with unk tokens')
    args = parser.parse_args()

    for input_file_name in args.input_file_names:
        conllu_sents = pyconll.load.iter_from_file(input_file_name)
        all_the_words = Counter()
        for sent in tqdm(conllu_sents):
            for token in sent:
                if token.form:
                    # we're lower casing all vocabs for philosophical reasons;
                    # the model already gets enough information from the int rep
                    all_the_words[token.form.lower()] += 1
        vocab_out = []
        # only take words which appear min_num_occurences times
        for word, num_occurences in tqdm(all_the_words.most_common()):
            if num_occurences < args.min_num_occurrences:
                break
            vocab_out.append(word)

        # max vocab size
        vocab_out = vocab_out[:args.max_vocab_size]

        input_file_root = \
            os.path.basename(os.path.splitext(input_file_name)[0])
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '.vocab.txt')
        with open(output_file_name, 'w') as out_file:
            out_file.write('\n'.join(vocab_out))

if __name__ == '__main__':
    main()
