import argparse
import os
import re
import spacy

from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='Process and tokenize into'
                                     'sents')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_names', nargs='*', help='writing'
                        'prompts story files, one story per line')
    args = parser.parse_args()

    nlp = spacy.load('en_core_web_sm')

    # regexes
    match_newline_tokens = re.compile(r"(<newline>)(\s\1){0,}")
    match_ellipses = re.compile(r"\s\.\.\.\s")
    # To make sure we don't loose the surrounding letters sub using r"\1'\3"
    match_single_close_quote = re.compile(r"(\w)(\s’\s)(\w{1,2}\b)")
    match_double_open_quote = re.compile(r"``")
    match_double_close_quote = re.compile(r"''")

    for input_file_name in args.input_file_names:
        with open(input_file_name) as in_file:
            stories = in_file.readlines()
        # write to file throughout the loop
        input_file_root = \
            os.path.basename(os.path.splitext(input_file_name)[0])
        output_file_name = os.path.join(args.output_dir_name,
                                        input_file_root +
                                        '.tok.txt')
        with open(output_file_name, 'w') as out_file:
            for story in tqdm(stories):
                # is it bad that we edit the same variable?
                story = story.strip()
                # A whole bunch of regex substitutions
                story = re.sub(match_newline_tokens, r"\\n", story)
                # run this twice in case there are two in a row
                story = re.sub(match_ellipses, r" … ", story)
                story = re.sub(match_ellipses, r" … ", story)
                story = re.sub(match_single_close_quote, r"\1'\3", story)
                story = re.sub(match_double_open_quote, r"“", story)
                story = re.sub(match_double_close_quote, r"”", story)
                story_doc = nlp(story)
                sents = []
                num_tokens = 0
                for sent in story_doc.sents:
                    tokens = [token.text for token in sent]
                    num_tokens += len(tokens)
                    # like in the original we limit to 1,000 tokens
                    if num_tokens >= 1000:
                        break
                    sents.append(' '.join(tokens))
                out_file.write('\n'.join(sents) + "\n\n")

if __name__ == '__main__':
    main()
