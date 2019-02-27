import argparse
import os

import jsonlines

def main():
    parser = argparse.ArgumentParser(description='combine multiple files into '
                                     'a json lines file for prodigy')
    # parser.add_argument('-o', '--output_dir_name', help='output directory')
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

    out_dicts = []
    for this_id, this_input, this_output in zip(ids, model_inputs,
                                                model_outputs):
        this_dict = {'id': this_id}
        this_dict['input'] = {'text': this_input}
        this_dict['output'] = {'text': this_output}
        out_dicts.append(this_dict)

    output_file_name = os.path.join(args.outputs_file_name + '.jsonl')
    with jsonlines.open(output_file_name, mode='w') as out_file:
        out_file.write(out_dicts)

if __name__ == '__main__':
    main()
