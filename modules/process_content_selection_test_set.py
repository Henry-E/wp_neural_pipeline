import argparse
import os
import re
from tqdm import tqdm

def get_mr_source_tokens(e2e_mr):
    mr_tokens = []
    for act in e2e_mr:
        # maybe replace the replace with a strip instead?
        act_type = act[0:act.find('[')].strip()
        # we're tokenizing the two word act types
        act_type = re.sub(r'(family|eat|price)', r'\1 ', act_type)
        mr_tokens.extend(act_type.split())
        if act_type == 'name' or act_type == 'near':
            # the delexicalized act types
            mr_tokens.append('x' + act_type)
        else:
            value = act[act.find('[')+1:act.find(']')]
            value = re.sub(r'£', r'£ ', value)
            value = re.sub(r'-', r' - ', value)
            mr_tokens.append(value)
        mr_tokens.append(',')
    # We remove the final , comma at the end of the list
    mr_tokens.pop()
    return ' '.join(mr_tokens)

def main():
    parser = argparse.ArgumentParser(description='delex and tokenize MR')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_name', help='just mrs')
    args = parser.parse_args()

    with open(args.input_file_name) as in_file:
        mrs = [line.strip().split(', ') for line in in_file]
    out_mrs = [get_mr_source_tokens(mr) for mr in mrs]

    output_file_name = os.path.join(args.output_dir_name,
                                    'testset_mrs.delex.tok.uniq')
    with open(output_file_name, 'w') as out_file:
        out_file.write('\n'.join(out_mrs))
        
if __name__ == '__main__':
    main()
