import argparse
import os
import re
import concurrent.futures
import spacy

from tqdm import tqdm

# regexes
match_newline_tokens = re.compile(r"(<newline>)(\s\1){0,}")
match_ellipses = re.compile(r"\s\.\.\.\s")
# To make sure we don't loose the surrounding letters sub using r"\1'\3"
match_single_close_quote = re.compile(r"(\w)(\s’\s)(\w{1,2}\b)")
match_double_open_quote = re.compile(r"``")
match_double_close_quote = re.compile(r"''")
# Again join at the end using \1\2, these special contractions get double
# tokenized by spacy. ugh
match_special_contractions = re.compile(r"(\b\w+)\s('(ve|m))\b")
# this is for splitting apart quotations and newline characters
match_split_chars = re.compile(r"(“|”|newwline)")

# This probably shouldn't be a global variable but I'm used to putting stuff in
# the main() function but it's difficult to pass stuff around with the new
# execute pooled function
nlp = spacy.load('en_core_web_sm')

# TODO
# Add back in the writing prompt input option once we get multithreading
# working ok
def sent_tok_story(story):
    story = story.strip()
    # A whole bunch of regex substitutions
    story = re.sub(match_newline_tokens, r"newwline", story)
    # run this twice in case there are two in a row
    story = re.sub(match_ellipses, r" … ", story)
    story = re.sub(match_ellipses, r" … ", story)
    story = re.sub(match_single_close_quote, r"\1'\3", story)
    story = re.sub(match_double_open_quote, r"“", story)
    story = re.sub(match_double_close_quote, r"”", story)
    story = re.sub(match_special_contractions, r"\1\2", story)
    # TODO
    # Maybe we can speed things up by setting a max number of
    # tokens before running the spacy tokenizer. Maybe split on
    # spaces and limit to 1,100 tokens, then rejoin.
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
    # Here we break apart quotation marks and newlines into their
    # own separate lines
    final_lines = []
    for sent in sents:
        split_sent = re.split(match_split_chars, sent)
        split_sent = [this.strip() for this in split_sent]
        split_sent = list(filter(None, split_sent))
        final_lines.extend(split_sent)
    return final_lines

def main():
    parser = argparse.ArgumentParser(description='Process and tokenize into'
                                     'sents')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_names', nargs='*', help='writing'
                        'prompts and story files, one story per line')
    parser.add_argument('--wp_file_name', help='writing prompts file')
    parser.add_argument('--stories_file_name', help='stories file')
    parser.add_argument('--max_num_stories', type=int, default=100, help='how many stories to'
                        'process')
    args = parser.parse_args()



    # for input_file_name in args.input_file_names:
    #     file_extension = os.path.splitext(input_file_name)[1]
    #     if 'wp_source' in file_extension:
    #         writing_prompts_file_name = input_file_name
    #     else if 'wp_target'

    # TODO
    # maybe have a check that wp and stories come from the same data split
    wp_file_root = \
        os.path.basename(os.path.splitext(args.wp_file_name)[0])
    output_file_name = os.path.join(args.output_dir_name,
                                    wp_file_root +
                                    '.tok.txt')

    with open(args.wp_file_name) as wp_file, open(args.stories_file_name) as \
        stories_file, open(output_file_name, 'w') as out_file:

        stories = stories_file.readlines()

        # with open(input_file_name) as in_file:
        #     stories = in_file.readlines()
        # write to file throughout the loop
        # input_file_root = \
        #     os.path.basename(os.path.splitext(input_file_name)[0])
        # output_file_name = os.path.join(args.output_dir_name,
        #                                 input_file_root +
        #                                 '.tok.txt')
        # with open(output_file_name, 'w') as out_file:
        #     for story in tqdm(stories):
                # is it bad that we edit the same variable?
        sentence_tokenized_stories = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            num_tokenized_stories = 0
            pbar = tqdm(total=args.max_num_stories)
            for sentence_tokenized_story in executor.map(sent_tok_story,
                                                         stories,
                                                         chunksize=1001):
                sentence_tokenized_stories.append('\n'.join(sentence_tokenized_story))
                num_tokenized_stories += 1
                pbar.update(1)
                if num_tokenized_stories >= args.max_num_stories:
                    break
        out_file.write('\n\n'.join(sentence_tokenized_stories) + "\n\n")

if __name__ == '__main__':
    main()
