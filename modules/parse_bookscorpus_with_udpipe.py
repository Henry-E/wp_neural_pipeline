import argparse
import os
import json
import subprocess
from itertools import islice
from tqdm import tqdm

def split_corpus(path, shard_size):
    with open(path, 'r') as in_file:
        while True:
            shard = list(islice(in_file, shard_size))
            if not shard:
                break
            yield shard

def main():
    parser = argparse.ArgumentParser(description='tag, filter and create '
                                     'source')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_names', nargs='*', help='story file')
    parser.add_argument('-m', '--model_name',
                        default='english-ewt-ud-2.3-181115',
                        type=str,
                        help='udpipe model name from: '
                        'http://lindat.mff.cuni.cz/services/udpipe/api/models')
    args = parser.parse_args()
    # num_stories_per_chunk = 300
    shard_size = 5000
    num_shards = 14546
    model = 'model={}'.format(args.model_name)
    # in this case, the data is already tokenized, with sents on separate lines
    udpipe_api_template = ['curl', '-F', 'data=@{upload_file_name}',
                           '-F', model,
                           '-F', 'input=horizontal',
                           '-F', 'tagger=', '-F', 'parser=',
               'http://lindat.mff.cuni.cz/services/udpipe/api/process']
    for input_file_name in args.input_file_names:
        text_shards = split_corpus(input_file_name, shard_size)
        for this_shard in tqdm(text_shards, total=num_shards):
            # sometimes the udpipe api will return an illformed json string
            # even though there's nothing wrong with the input. Rerunning the
            # same input again returns the correct output. This happens very
            # randomly and very rarely. So we just try except and rerun if it
            # fails.
            still_running = True
            while still_running:
                try:
                    string_chunk = ''.join(this_shard)
                # with open(input_file_name) as in_file:
                #     stories = in_file.read().split('\n\n')
                #     num_story_chunks = int(round(len(stories) / num_stories_per_chunk))
                #     string_chunks = ['\n\n'.join(stories[i::num_story_chunks]) for i in
                #                      range(num_story_chunks)]
                    # for string_chunk in string_chunks:
                    udpipe_api_call = udpipe_api_template
                    upload_file_name = os.path.join(args.output_dir_name,
                                                    'temp_upload_file.txt')
                    with open(upload_file_name, 'w') as out_file:
                        out_file.write(string_chunk)
                    # this line length formatting is starting to look ridiculous
                    udpipe_api_call[2] = \
                        udpipe_api_call[2].format( \
                                              upload_file_name=upload_file_name)
                    # TODO
                    # We still need to add a check to the subprocess call in case
                    # we send too much data by accident
                    udpipe_json_results = subprocess.run(udpipe_api_call,
                                                         stdout=subprocess.PIPE)
                                                         # stderr=subprocess.STDOUT)
                    udpipe_json_results = udpipe_json_results.stdout.decode()
                    udpipe_results = json.loads(udpipe_json_results)['result']
                    # udpipe_strings = udpipe_results.split('\n\n')
                    # Note: for now we won't remove boiler plate comments
                    # there's some boiler plate information in the first two lines
                    # returned by the udpipe api that we need to remove
                    # import ipdb; ipdb.set_trace()
                    # udpipe_strings[0] = '\n'.join(udpipe_strings[0].split('\n')[2:])
                    # conll = []
                    # sentences = []
                    # for full_conll in udpipe_strings:
                    #     full_conll = full_conll.split('\n')
                    #     if '' in  full_conll:
                    #         continue
                    #     conll.append('\n'.join(full_conll[2:]))
                    #     sentences.append('\n'.join(full_conll[:2]))
                    model_name_simplified = '_'.join(args.model_name.split('-')[1:-1])
                    input_file_basename = os.path.basename(input_file_name)
                    # Simon's deep parser script breaks if the file name doesn't
                    # have conllu, specifically at the end. Before we had conll
                    output_file_name = os.path.join(args.output_dir_name,
                                                    input_file_basename + '.' +
                                                    model_name_simplified +
                                                    '.conllu')
                    with open(output_file_name, 'a') as out_file:
                        out_file.write(udpipe_results)
                    # output_file_name = os.path.join(args.output_dir_name,
                    #                                 input_file_basename + '.' +
                    #                                 model_name_simplified +
                    #                                 '.sentences')
                    # with open(output_file_name, 'a') as out_file:
                    #     out_file.write('\n\n'.join(sentences) + '\n\n')
                    # making sure to clean up after the uploads are finished
                    os.remove(upload_file_name)
                    still_running = False
                except ValueError:
                    print("ran into another json error, rerunning agian")
        # For posterity
        # We need to do smaller API calls, otherwise we'll end up overwhelming
        # the API and getting rejected. We did a 1mb file that took about 7
        # minutes to process and returned about 13mb to STDOUT. The alternative
        # is that we load up smaller chunks of text send them directly in the
        # string rather than as a file. We're waiting to her back from the devs
        # about what approach is best.

if __name__ == '__main__':
    main()
