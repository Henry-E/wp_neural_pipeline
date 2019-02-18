import argparse
import os
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='filter longer sents')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument( '--input_src_file_name', help='conllu file')
    parser.add_argument( '--input_tgt_file_name', help='conllu file')
    args = parser.parse_args()

    with open(args.input_src_file_name) as in_src, open(args.input_tgt_file_name) as in_tgt:
        tgt_out = []
        previous_line = ''
        for src, tgt in zip(in_src, in_tgt):
            if not previous_line:
                previous_line = src
                tgt_out.append(tgt)
                continue
            if src != previous_line:
                tgt_out.append('\n')
            previous_line = src
            tgt_out.append(tgt)
    print("warning this adds an extra line before the final line, just delete it manually")

    output_file_name = args.input_tgt_file_name + '.multiref'
    with open(output_file_name, 'w') as out_file:
        out_file.write(''.join(tgt_out))

if __name__ == '__main__':
    main()
