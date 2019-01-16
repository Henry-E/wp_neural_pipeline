import argparse
import os
import re
from collections import deque
import pyconll
from pyconll.tree import SentenceTree
from tqdm import tqdm

def linearize_tree(node):
    linearization = []
    linearization.append(node.data.id)
    # TODO later on we will order the children based on the order they appeared
    # in the original sentence
    child_nodes = node.children
    for child in child_nodes:
        linearization.extend(linearize_tree(child))
    return linearization

def process_deep_ud(deep_ud):
    deep_tree = SentenceTree(deep_ud).tree
    linearized_ids = linearize_tree(deep_tree)
    linearized_deep_tokens = []
    for tok_id in linearized_ids:
        # we index using a string, could also do tok_id-1 to index to 0
        if deep_ud[str(tok_id)].form:
            linearized_deep_tokens.append(deep_ud[str(tok_id)].form)
    return linearized_deep_tokens

def get_ud_sent_tokens(sentence):
    tokens = []
    for token in sentence:
        if token.form:
            tokens.append(token.form)
        else:
            # it seemingly mistakes underscores for None objects
            tokens.append('_')
    return tokens


def main():
    parser = argparse.ArgumentParser(description='create source and target')
    parser.add_argument('--udpipe_file_name', help='udpipe output')
    parser.add_argument('--deep_parser_file_name', help='deep parser output')
    parser.add_argument('--content_selection_dir_name', help='output directory')
    parser.add_argument('--surface_realization_dir_name', help='output dir')
    args = parser.parse_args()

    with open(args.udpipe_file_name) as in_file:
        udpipe_input = in_file.read().replace('# newdoc\n','')
    sections = udpipe_input.split('# newpar')
    deep_sents = pyconll.load.iter_from_file(args.deep_parser_file_name)

    content_selection_src = []
    content_selection_tgt = []
    surface_realization_src = []
    surface_realization_tgt = []

    # we read it's much quicker to join a list of strings than keep a
    # continuously updating string https://waymoot.org/home/python_string/
    for section in tqdm(sections):
        this_section = pyconll.load.iter_from_string(section)
        # keeping a rolling context with max length of src + tgt of 200
        context_sents = deque()
        num_context_sents_toks = 0
        for sent in this_section:
            deep_sent_conll = next(deep_sents)
            deep_sent_tokens = process_deep_ud(deep_sent_conll)
            ud_sent_tokens = get_ud_sent_tokens(sent)
            num_deep_sent_toks = len(deep_sent_tokens)
            if num_context_sents_toks + num_deep_sent_toks > 200:
                # remove sentences until total tokens is under 200
                while True:
                    if 'new_sent' not in context_sents:
                        # it's possible 1 sent + 1 tgt is > 200
                        # And we don't really want this so we reset the context
                        # and ignore this source target pair
                        context_sents = deque()
                        num_context_sents_toks = 0
                        print(num_context_sents_toks, num_deep_sent_toks)
                        break
                    cur_token = context_sents.popleft()
                    num_context_sents_toks -= 1
                    if cur_token == 'new_sent' and \
                         num_context_sents_toks + num_deep_sent_toks <= 200:
                        break
            # We've decided to avoid deep representations with greater than 35
            # tokens. This accounts for about 2.5% of deep representations
            if num_deep_sent_toks <= 35:
                # needs at least 1 sentence context
                if context_sents:
                    content_selection_src.append(' '.join(context_sents))
                    content_selection_tgt.append(' '.join(deep_sent_tokens))
                surface_realization_src.append(' '.join(deep_sent_tokens))
                surface_realization_tgt.append(' '.join(ud_sent_tokens))
            num_ud_sent_tokens = len(ud_sent_tokens)
            if context_sents:
                context_sents.extend(['new_sent'] + ud_sent_tokens)
                num_context_sents_toks += num_ud_sent_tokens + 1
            else:
                context_sents.extend(ud_sent_tokens)
                num_context_sents_toks += num_ud_sent_tokens

    input_file_root = \
        os.path.basename(os.path.splitext(args.deep_parser_file_name)[0])

    content_selection_src_file_name = \
        os.path.join(args.content_selection_dir_name,
                     input_file_root + '.content_selection.src')
    with open(content_selection_src_file_name, 'w') as out_file:
        out_file.write('\n'.join(content_selection_src))
    content_selection_tgt_file_name = \
        os.path.join(args.content_selection_dir_name,
                     input_file_root + '.content_selection.tgt')
    with open(content_selection_tgt_file_name, 'w') as out_file:
        out_file.write('\n'.join(content_selection_tgt))

    surface_realization_src_file_name = \
        os.path.join(args.surface_realization_dir_name,
                     input_file_root + '.surface_realization.src')
    with open(surface_realization_src_file_name, 'w') as out_file:
        out_file.write('\n'.join(surface_realization_src))
    surface_realization_tgt_file_name = \
        os.path.join(args.surface_realization_dir_name,
                     input_file_root + '.surface_realization.tgt')
    with open(surface_realization_tgt_file_name, 'w') as out_file:
        out_file.write('\n'.join(surface_realization_tgt))


if __name__ == '__main__':
    main()
