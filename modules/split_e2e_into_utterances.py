import argparse
import os
import csv

def main():
    parser = argparse.ArgumentParser(description='''take in the e2e csvs and
                                     output the utterances in a format suitable
                                     for udpipe parsing''')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_names', nargs='*',
                        help='csv files')
    args = parser.parse_args()

    for input_file_name in args.input_file_names:
        with open(input_file_name) as in_file:
            lines_reader = csv.reader(in_file)
            # skip the header
            next(lines_reader)
            utterances = []
            for line in lines_reader:
                if line:
                    utterances.append(line[1])
        input_file_root = \
            os.path.basename(os.path.splitext(input_file_name)[0])
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root + '.utterances')
        with open(output_file_name, 'w') as out_file:
            # we use a double new line delimiter so that each utterances is
            # parsed as a new paragraph by UDpipe
            out_file.write('\n\n'.join(utterances))

if __name__ == '__main__':
    main()
