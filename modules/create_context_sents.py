import argparse
import os
import pyconll
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='extract tokenized sents from'
                                     'conllu')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_name', help='conllu file')
    args = parser.parse_args()

    stories = pyconll.iter_from_file(args.input_file_name)

    tokenized_sents = []
    for sentence in tqdm(stories):
        import ipdb; ipdb.set_trace()
        tokens = []
        for token in sentence:
            if token.form:
                tokens.append(token.form)
            else:
                # it mistakes underscores for None objects
                tokens.append('_')

        tokenized_sent = ' '.join(tokens)
        tokenized_sents.append(tokenized_sent)

    input_file_root = \
        os.path.basename(os.path.splitext(args.input_file_name)[0])
    output_file_name = os.path.join(args.output_dir_name,
                                    input_file_root +
                                    '.sents')
    with open(output_file_name, 'w') as out_file:
        out_file.write('\n'.join(tokenized_sents))

if __name__ == '__main__':
    main()
