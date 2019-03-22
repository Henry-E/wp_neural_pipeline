import argparse
import os
import re
import json
from collections import Counter

def main():
    parser = argparse.ArgumentParser(description='get readability stats')
    parser.add_argument('-i', '--input_file_name', help='db-out jsonl file')
    args = parser.parse_args()

    readability_stats = Counter()
    for line in open(args.input_file_name, encoding='utf8'):
        record = json.loads(line)
        # then it's an e2e
        for model_type in ['e2e', 'ta']:
            if not re.match(r'.*{}$'.format(model_type), record['id']):
                continue
            if record['answer'] == 'ignore':
                readability_stats['{}_equal'.format(model_type)] += 1
            elif record['answer'] == 'accept' and \
                    record['mapping']['B'] == 'accept' or \
                    record['answer'] == 'reject' and \
                    record['mapping']['B'] == 'reject':
                readability_stats['{}_better'.format(model_type)] += 1
            readability_stats['{}_total_annotations'.format(model_type)] += 1
    for key, value in readability_stats.items():
        print(key, value)

if __name__ == '__main__':
    main()
