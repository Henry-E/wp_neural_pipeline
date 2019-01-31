import argparse
import os
import re
from collections import deque
import pyconll
from pyconll.tree import SentenceTree
from tqdm import tqdm

def linearize_tree(node, scopes_to_close=0):
    linearization = []
    if node.data.form:
        linearization.append(str(node.data.id))
    # TODO Add scoping markers
    # Remove empty nodes with form "_" them because they're missing original
    # IDs in the feats column
    child_nodes = [child for child in node.children if child.data.form]
    # we want child nodes to appear in the order they appeared in the original
    # sentence. This will simplify things for the model a bit
    sorted_child_nodes = sorted(child_nodes,
                                key=lambda child:
                                int(list(child.data.feats['original_id'])[0]))
    # More than one child or the sole child has its own children
    if sorted_child_nodes and (len(sorted_child_nodes) > 1 or
                               sorted_child_nodes[0].children):
        # Open scope
        linearization.append('_(')
    # if there's no more child nodes
    elif not sorted_child_nodes:
        # Close scopes
        linearization.extend([')_'] * scopes_to_close)
    for k, child in enumerate(sorted_child_nodes):
        # if it's the last one and we just opened a scope
        if k == len(sorted_child_nodes) - 1 and (len(sorted_child_nodes) > 1 or
                                                 sorted_child_nodes[0].children):
            scopes_to_close += 1
            linearization.extend(linearize_tree(child, scopes_to_close))
        elif len(sorted_child_nodes) == 1:
            linearization.extend(linearize_tree(child, scopes_to_close))
        else:
            # if it's not the last one then it's not going to have anything to
            # do with closing scopes
            linearization.extend(linearize_tree(child))
    return linearization

def process_deep_ud(deep_ud, args, vocab=None):
    if args.original_sentence_order:
        tokens = [token for token in deep_ud if token.form]
        linearized_ids = \
            [str(token.id) for token in \
             sorted(tokens,
                    key=lambda token: int(list(token.feats['original_id'])[0]))]
    else:
        deep_tree = SentenceTree(deep_ud).tree
        linearized_ids = linearize_tree(deep_tree)
        if args.add_scope_markers:
            pass
        else:
            # we determined it was easier to simpler filter out the scoping
            # markers than to add a whole bunch of special statements in the
            # original function
            linearized_ids = [token for token in linearized_ids
                              if token != '_(' or token != ')_']

    linearized_deep_tokens = []
    for tok_id in linearized_ids:
        # TODO
        # What to do with the scoping brackets
        if tok_id == '_(' or tok_id == ')_':
            # linearized_deep_tokens.append(tok_id + '￨' + '_')
            linearized_deep_tokens.append(tok_id)
            continue
        # we index using a string, could also do tok_id-1 to index to 0
        this_form = deep_ud[tok_id].form
        if not this_form:
            pass
        if vocab and this_form in vocab:
            linearized_deep_tokens.append(this_form)
        elif vocab:
            if deep_ud[tok_id].xpos:
                # TODO
                # add unk + xpos
                linearized_deep_tokens.append('unk_' + deep_ud[tok_id].xpos)
            else:
                linearized_deep_tokens.append('unk')
        else:
            linearized_deep_tokens.append(this_form)
        # this_deprel = deep_ud[tok_id].deprel
        # if this_deprel:
        #     linearized_deep_tokens[-1] = linearized_deep_tokens[-1] + \
        #                                 '￨' + this_deprel
        # else:
        #     linearized_deep_tokens[-1] = linearized_deep_tokens[-1] + \
        #                                 '￨' + '_'
    return linearized_deep_tokens

def  get_ud_sent_tokens(sentence, vocab=None):
    tokens = []
    for token in sentence:
        this_form = token.form
        if not this_form:
            pass
        if vocab and this_form in vocab:
            tokens.append(this_form)
        elif vocab:
            if token.xpos:
                tokens.append('unk_' + token.xpos)
            else:
                tokens.append('unk')
        else:
            tokens.append(this_form)
    return tokens


def main():
    parser = argparse.ArgumentParser(description='create source and target')
    parser.add_argument('-f', '--filtered_udpipe_file_name', help='filtered udpipe output')
    parser.add_argument('-d', '--deep_parser_file_name', help='deep parser output')
    parser.add_argument('-c', '--content_selection_dir_name', help='output directory')
    parser.add_argument('-s', '--surface_realization_dir_name', help='output dir')
    parser.add_argument('--add_scope_markers', action='store_true',
                        help='add parentheses around linearized nodes')
    parser.add_argument('--original_sentence_order', action='store_true',
                        help='order tokens based on the original sentence')
    parser.add_argument('--vocab_file', default='',
                        help='vocab file with one word per line')
    args = parser.parse_args()

    # with open(args.filtered_udpipe_file_name) as in_file:
    #     udpipe_input = in_file.read().replace('# newdoc\n', '')
    # sections = udpipe_input.split('# new_par')
    ud_sents = pyconll.load.iter_from_file(args.filtered_udpipe_file_name)
    deep_sents = pyconll.load.iter_from_file(args.deep_parser_file_name)

    # TODO
    # load file containing tokens in vocab into a set
    vocab = []
    if args.vocab_file:
        vocab = set(line.strip() for line in open(args.vocab_file))

    content_selection_src = []
    content_selection_tgt = []
    surface_realization_src = []
    surface_realization_tgt = []

    # we read it's much quicker to join a list of strings than keep a
    # continuously updating string https://waymoot.org/home/python_string/

    # TODO We realize now it would be quicker to load an iter of both files.
    # and figure out how to check the comments above each conllu for special
    # markers to indicate that it's a new paragraph
    # for section in tqdm(sections):
        # this_section = pyconll.load.iter_from_string(section)
        # keeping a rolling context with max length of src + tgt of 200
    context_sents = deque()
    num_context_sents_toks = 0
    for sent in tqdm(ud_sents):
        # TODO
        # Get a better paragraph / delimiter scheme that's more in line with
        # what pyconll expects
        # Reset the values each new paragraph / section
        if sent.meta_present("new_par"):
            context_sents = deque()
            num_context_sents_toks = 0
        deep_sent_conll = next(deep_sents)
        deep_sent_tokens = process_deep_ud(deep_sent_conll, args, vocab)
        ud_sent_tokens = get_ud_sent_tokens(sent, vocab)
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
    # whether it's .train, .dev or .test
    input_file_data_split = os.path.splitext(args.deep_parser_file_name)[1]

    content_selection_src_file_name = \
        os.path.join(args.content_selection_dir_name,
                     input_file_root + '.content_selection'
                     + input_file_data_split + '.src')
    with open(content_selection_src_file_name, 'w') as out_file:
        out_file.write('\n'.join(content_selection_src))
    content_selection_tgt_file_name = \
        os.path.join(args.content_selection_dir_name,
                     input_file_root + '.content_selection'
                     + input_file_data_split + '.tgt')
    with open(content_selection_tgt_file_name, 'w') as out_file:
        out_file.write('\n'.join(content_selection_tgt))

    surface_realization_src_file_name = \
        os.path.join(args.surface_realization_dir_name,
                     input_file_root + '.surface_realization'
                     + input_file_data_split + '.src')
    with open(surface_realization_src_file_name, 'w') as out_file:
        out_file.write('\n'.join(surface_realization_src))
    surface_realization_tgt_file_name = \
        os.path.join(args.surface_realization_dir_name,
                     input_file_root + '.surface_realization'
                     + input_file_data_split + '.tgt')
    with open(surface_realization_tgt_file_name, 'w') as out_file:
        out_file.write('\n'.join(surface_realization_tgt))


if __name__ == '__main__':
    main()
