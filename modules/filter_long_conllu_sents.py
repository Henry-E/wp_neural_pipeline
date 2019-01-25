import argparse
import os
import re
from tqdm import tqdm

def split_conllu(path):
    separator = '\n'
    comment_lines = re.compile(r"^#")
    with open(path, 'r') as in_file:
        conllu_sent = []
        for line in in_file:
            if comment_lines.match(line):
                continue
            if line == separator:
                if conllu_sent:
                    yield ''.join(conllu_sent)
                    conllu_sent = []
            else:
                conllu_sent.append(line)
        if conllu_sent:
            yield ''.join(conllu_sent)

def main():
    parser = argparse.ArgumentParser(description='filter longer sents')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_name', help='conllu file')
    args = parser.parse_args()

    input_file_root = \
            os.path.basename(os.path.splitext(args.input_file_name)[0])
    output_file_name = os.path.join(args.output_dir_name,
                                    input_file_root + '.filter.conllu')

    # Anything 100 length or longer get left out
    long_sents = re.compile(r"\n100\t")
    conllu_sents = split_conllu(args.input_file_name)
    with open(output_file_name, 'w') as out_file:
        sent_id = 1
        for this_sent in tqdm(conllu_sents):
            if long_sents.search(this_sent):
                out_file.write('# new_par\n')
                continue
            this_out = ''.join(['# sent_id = ', str(sent_id), '\n', this_sent, '\n'])
            out_file.write(this_out)
            sent_id += 1
    print("processed this many sentences, lol: ", sent_id - 1)
        
if __name__ == '__main__':
    main()
