import argparse
import os
import re
from collections import deque
import pyconll
from pyconll.tree import SentenceTree
from tqdm import tqdm

def linearize_tree(node, args):
    linearization = []
    linearization.append(node.data.id)
    # TODO Add scoping markers
    # we want child nodes to appear in the order they appeared in the original
    # sentence. This will simplify things for the model a bit
    child_nodes = sorted(node.children,
                         key=lambda child:
                         int(list(child.data.feats['original_id'])[0]))
    for child in child_nodes:
        linearization.extend(linearize_tree(child, args))
    return linearization

def process_deep_ud(deep_ud, args):
    if args.original_sentence_order:
        linearized_ids = \
            [str(node.id) for node in \
             sorted(deep_ud,
                    key=lambda node: int(list(node.feats['original_id'])[0]))]
    else:
        deep_tree = SentenceTree(deep_ud).tree
        linearized_ids = linearize_tree(deep_tree, args)
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
    parser.add_argument('-u', '--udpipe_file_name', help='udpipe output')
    parser.add_argument('-d', '--deep_parser_file_name', help='deep parser output')
    parser.add_argument('-c', '--content_selection_dir_name', help='output directory')
    parser.add_argument('-s', '--surface_realization_dir_name', help='output dir')
    parser.add_argument('--add_scope_markers', action='store_true',
                        help='add parentheses around linearized nodes')
    parser.add_argument('--original_sentence_order', action='store_true',
                        help='order tokens based on the original sentence')
    args = parser.parse_args()

    with open(args.udpipe_file_name) as in_file:
        udpipe_input = in_file.read().replace('# newdoc\n', '')
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
            deep_sent_tokens = process_deep_ud(deep_sent_conll, args)
            ud_sent_tokens = get_ud_sent_tokens(sent)
            num_deep_sent_toks = len(deep_sent_tokens)
            if num_context_sents_toks > 150:
                # remove sentences until total tokens is under 150
                while True:
                    if 'new_sent' not in context_sents:
                        # this techincally speaking shouldn't happen because we
                        # have already filtered out all sentences with more
                        # than 100 tokens
                        context_sents = deque()
                        num_context_sents_toks = 0
                        print(num_context_sents_toks, num_deep_sent_toks)
                        break
                    cur_token = context_sents.popleft()
                    num_context_sents_toks -= 1
                    if cur_token == 'new_sent' and \
                         num_context_sents_toks <= 150:
                        break
            # We've decided to avoid deep representations with greater than 35
            # tokens. The percentage this accounts for varies based on dataset
            num_ud_sent_tokens = len(ud_sent_tokens)
            # TODO change from 35 to allow for longer when scoping
            if num_deep_sent_toks <= 35:
                # needs at least 1 sentence context
                if context_sents:
                    content_selection_src.append(' '.join(context_sents))
                    content_selection_tgt.append(' '.join(deep_sent_tokens))
                # we limit target surfacer realization sents to 50 tokens
                if num_ud_sent_tokens <= 50:
                    surface_realization_src.append(' '.join(deep_sent_tokens))
                    surface_realization_tgt.append(' '.join(ud_sent_tokens))
            if context_sents:
                context_sents.extend(['new_sent'] + ud_sent_tokens)
                num_context_sents_toks += 1 + num_ud_sent_tokens
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
