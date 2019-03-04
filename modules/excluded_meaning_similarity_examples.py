import argparse
import os
import difflib

import jsonlines

def create_annotation(this_id, this_input, this_output, metadata=None):
    annotation = {}
    annotation['id'] = this_id
    annotation['input'] = {'text': this_input}
    annotation['accept'] = {'text': this_output}
    annotation['reject'] = {'text': this_input}
    annotation['mapping'] = {'A': 'accept', 'B': 'reject'}
    annotation['answer'] = 'accept'
    annotation['meta'] = metadata
    return annotation

def clean_string(sent):
    out_sent = sent.lower()
    out_sent = out_sent.replace('-', ' ')
    # remove any extra whitespace
    out_sent = ' '.join(out_sent.split())
    return out_sent

def main():
    parser = argparse.ArgumentParser(description='create examples to exclude'
                                     'from prodigy meaning similarity'
                                     ' evaluation')
    parser.add_argument('--ids_file_name', help='list of ids')
    parser.add_argument('--inputs_file_name', help='list of reference sents')
    parser.add_argument('--outputs_file_name', help='list of generated'
                        'sents, could also be reference sent again')
    args = parser.parse_args()

    with open(args.ids_file_name) as in_file:
        ids = [line.rstrip() for line in in_file]
    with open(args.inputs_file_name) as in_file:
        model_inputs = [line.rstrip() for line in in_file]
    with open(args.outputs_file_name) as in_file:
        model_outputs = [line.rstrip() for line in in_file]

    contains_unk_ids = []
    for this_id, gen_sent in zip(ids, model_outputs):
        if 'unk' in gen_sent:
            contains_unk_ids.append(this_id)

    acceptable_differences = ['', ',', '.', 'a', 'an', 'the']
    matching_sent_ids = []
    very_similar_sent_ids = []
    for this_id, ref_sent, gen_sent in zip(ids, model_inputs, model_outputs):
        ref_sent = clean_string(ref_sent)
        gen_sent = clean_string(gen_sent)
        if this_id in contains_unk_ids:
            continue
        changes = []
        contiguous_changes = ['']
        for i, s in enumerate(difflib.ndiff(
                ref_sent.lower(), gen_sent.lower())):
            if s[0] == ' ':
                contiguous_changes.append('')
                continue
            elif s[0] == '-':
                changes.append('Delete "{}" from position {}'.format(s[-1], i))
                contiguous_changes[-1] += s[-1]
            elif s[0] == '+':
                changes.append('Add "{}" from position {}'.format(s[-1], i))
                contiguous_changes[-1] += s[-1]
        # remove the empty strings acting as delimiters
        contiguous_changes = list(filter(None, contiguous_changes))
        num_contiguous_changes = len(contiguous_changes)
        num_changes = len(changes)
        if num_changes == 0:
            matching_sent_ids.append(this_id)
        elif all(elem.strip() in acceptable_differences for elem in
                 contiguous_changes):
            very_similar_sent_ids.append(this_id)
        #     print('{} => {}'.format(ref_sent, gen_sent))
        #     print(contiguous_changes)
    # print("There are this many similar sents ", len(very_similar_sent_ids))
    # print("Num that contains unks", len(contains_unk_ids))
    # print(len(ids))

    annotations = []
    for this_id, this_input, this_output in zip(ids, model_inputs,
                                                model_outputs):
        if this_id in contains_unk_ids:
            this_annotation = create_annotation(this_id, this_input,
                                                this_output, 'contains_unk')
        elif this_id in matching_sent_ids:
            this_annotation = create_annotation(this_id, this_input,
                                                this_output, 'matching_sent')
        elif this_id in very_similar_sent_ids:
            this_annotation = create_annotation(this_id, this_input,
                                                this_output, 'very_similar')
        else:
            continue
        annotations.append(this_annotation)

    output_file_name = os.path.join(args.outputs_file_name +
                                    '.meanining_similarity_exclude.jsonl')
    with jsonlines.open(output_file_name, mode='w') as out_file:
        for this in annotations:
            out_file.write(this)

if __name__ == '__main__':
    main()
