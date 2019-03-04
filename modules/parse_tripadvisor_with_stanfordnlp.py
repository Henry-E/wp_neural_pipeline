import argparse
import os

import stanfordnlp
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='tag, filter and create '
                                     'source')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_names', nargs='*', help='wikitext'
                                                            ' sentence files')
    args = parser.parse_args()

    nlp = stanfordnlp.Pipeline()
    output_file_name = os.path.join(args.output_dir_name,
                                    'trip_advisor_full_corpus.conllu')
    for input_file_name in tqdm(args.input_file_names):
        with open(input_file_name) as in_file:
            trip_advisor_reviews = [line.strip()[9:] for line in in_file if
                                    '<Content>' in line]
        review_conllu_strings = []
        for review in tqdm(trip_advisor_reviews):
            parsed_review = nlp(review)
            review_conllu_string = parsed_review.conll_file.conll_as_string()
            review_conllu_strings.append(review_conllu_string)
        with open(output_file_name, 'a') as out_file:
            out_file.write(''.join(review_conllu_strings))

if __name__ == '__main__':
    main()
