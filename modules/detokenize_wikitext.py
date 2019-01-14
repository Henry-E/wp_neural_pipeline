import argparse
import os
import re

from sacremoses import MosesDetokenizer

def main():
    parser = argparse.ArgumentParser(description='preprocess wikitext')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_names', nargs='*', help='wikitext')
    args = parser.parse_args()

    for input_file_name in args.input_file_names:
        with open(input_file_name) as wikitext:
            # We're assuming the lines have been stripped
            headers = re.compile(r"^=")
            sections = []
            current_lines = []
            for line in wikitext:
                line = line.strip()
                if not line:
                    continue
                if headers.match(line):
                    sections.append('\n'.join(current_lines))
                    current_lines = []
                    continue
                # This regex code was written before we had more experience
                # with it but we're too lazy to update it now.
                # undo lots of the tokenization
                line = re.sub('( @)|(@ )', '', line)
                # this appears to be a peculiar hyphen character that gets
                # missed by the other re.sub
                line = re.sub('( – )', '–', line)
                # this is another oddity we've noticed that the opening
                # bracket keeps its tokenized space even after detok
                line = re.sub('(\( )', '(', line)
                # the problem is that <unk> gets tokenized by udpipe as
                # < unk >, so we're using unk unless we can get a better
                # unk token
                line = re.sub('(<unk>)', 'unk', line)
                # import ipdb; ipdb.set_trace()
                detok_line = MosesDetokenizer().detokenize(line.split())
                current_lines.append(detok_line)
            if current_lines:
                sections.append('\n'.join(current_lines))
            # remove any empty sections
            sections = list(filter(None, sections))
        file_basename = os.path.basename(input_file_name)
        file_basename += '.detok'
        output_file_name = os.path.join(args.output_dir_name, file_basename)
        with open(output_file_name, 'w') as wikitext_output:
            wikitext_output.write('\n\n'.join(sections))

if __name__ == '__main__':
    main()
