import argparse
import os
import re
import csv
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
        # making sure to lower case all tokens
        this_form = this_form.lower()
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

def get_ud_sent_tokens(sentence, vocab=None):
    tokens = []
    for token in sentence:
        this_form = token.form
        if not this_form:
           continue 
        # lower casing all the tokens
        this_form = this_form.lower()
        if vocab and this_form in vocab:
            tokens.append(this_form)
        elif vocab:
            # We've decided to add deprel as well just to make the unk more
            # informative, maybe this will mess with things too much and we'll
            # have to switch back
            if token.xpos and token.deprel:
                tokens.append('_'.join(['unk', token.xpos]))
            else:
                tokens.append('unk')
        else:
            tokens.append(this_form)
    return tokens

def get_mr_source_tokens(e2e_mr, tokenize_mr=False):
    mr_tokens = []
    if tokenize_mr:
        pass
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
    else:
        # if we don't tokenize we turn everything into a single token, just
        # acttype_actvalue
        # we are testing getting rid of the comma delimiter as well
        for act in e2e_mr:
            act_type = act[0:act.find('[')].replace(' ', '')
            if act_type == 'name' or act_type == 'near':
                # the delexicalized act types
                mr_tokens.append('x' + act_type)
            else:
                # mr_tokens.append(act_type + ':')
                value = act[act.find('[')+1:act.find(']')].replace(' ', '')
                mr_tokens.append(act_type + '_' + value)
            # mr_tokens.append(',')
    if tokenize_mr:
        # We remove the final , comma at the end of the list
        mr_tokens.pop()
    return mr_tokens

def create_source_and_target_both(args):
    e2e_lines = csv.reader(open(args.e2e_data_file_name))
    # skip the header
    next(e2e_lines)
    deep_sents = pyconll.load.iter_from_file(args.deep_conllu_file_name)
    ud_sents = pyconll.load.iter_from_file(args.ud_conllu_file_name)
    vocab = set()
    if args.vocab_file:
        vocab = set(line.strip() for line in open(args.vocab_file))

    content_selection_src = []
    content_selection_tgt = []
    surface_realization_src = []
    surface_realization_tgt = []

    # We're keeping a rolling list in case an utterance is more than one
    # sentence
    deep_utterance = []
    for sent in tqdm(ud_sents):
        if sent.meta_present("newpar"):
            if deep_utterance:
                e2e_mr = next(e2e_lines)[0].split(', ')
                e2e_mr_tokens = get_mr_source_tokens(e2e_mr, args.tokenize_mr)
                content_selection_src.append(' '.join(e2e_mr_tokens))
                content_selection_tgt.append(' '.join(deep_utterance))
            deep_utterance = []
        deep_sent_conll = next(deep_sents)
        deep_sent_tokens = process_deep_ud(deep_sent_conll, args, vocab)
        ud_sent_tokens = get_ud_sent_tokens(sent, vocab)
        surface_realization_src.append(' '.join(deep_sent_tokens))
        surface_realization_tgt.append(' '.join(ud_sent_tokens))
        if deep_utterance:
            deep_utterance.extend(['new_sent'] + deep_sent_tokens)
        else:
            deep_utterance.extend(deep_sent_tokens)

    input_file_root = \
        os.path.basename(os.path.splitext(args.deep_conllu_file_name)[0])
    # whether it's .train, .dev or .test
    input_file_data_split = os.path.splitext(args.deep_conllu_file_name)[1]
    print("expect the end of the deep file to indicate what data split this is: ",
          input_file_data_split)

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


def create_source_and_target_surface_realization_only(args):
    # get num sents for tqdm
    with open(args.deep_conllu_file_name) as in_file:
        num_sents = sum(1 for line in in_file if len(line.strip()) == 0)
    deep_sents = pyconll.load.iter_from_file(args.deep_conllu_file_name)
    ud_sents = pyconll.load.iter_from_file(args.ud_conllu_file_name)
    vocab = set()
    if args.vocab_file:
        vocab = set(line.strip() for line in open(args.vocab_file))

    surface_realization_src = []
    surface_realization_tgt = []
    for ud_sent, deep_sent in tqdm(zip(ud_sents, deep_sents), total=num_sents):
        # TODO get de-unk vocab
        ud_sent_tokens = get_ud_sent_tokens(ud_sent, vocab)
        deep_sent_tokens = process_deep_ud(deep_sent, args, vocab)
        surface_realization_src.append(' '.join(deep_sent_tokens))
        surface_realization_tgt.append(' '.join(ud_sent_tokens))

    input_file_root = \
        os.path.basename(os.path.splitext(args.deep_conllu_file_name)[0])
    # whether it's .train, .dev or .test
    input_file_data_split = os.path.splitext(args.deep_conllu_file_name)[1]
    print("expect the end of the deep file to indicate what data split this is: ",
          input_file_data_split)

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

def main():
    parser = argparse.ArgumentParser(description='''process lots of input files
                                     to produce the source and target files for
                                     the different models we will train''')
    # inputs
    parser.add_argument('-e', '--e2e_data_file_name', help='original e2e file')
    parser.add_argument('-u', '--ud_conllu_file_name', help='ud_conllu output')
    parser.add_argument('-d', '--deep_conllu_file_name',
                        help='''deep parser output, expected to end in .dev or .train''')
    parser.add_argument('--vocab_file', default='',
                        help='vocab file with one word per line, optional')
    # outputs
    parser.add_argument('-c', '--content_selection_dir_name', help='output directory')
    parser.add_argument('-s', '--surface_realization_dir_name', help='output dir')
    # processing options
    parser.add_argument('--add_scope_markers', action='store_true',
                        help='add parentheses around linearized nodes')
    parser.add_argument('--original_sentence_order', action='store_true',
                        help='order tokens based on the original sentence')
    parser.add_argument('--tokenize_mr', action='store_true',
                        help='split apart the MR acts in small tokens')
    parser.add_argument('--surface_realization_only', action='store_true',
                        help='only process the src and tgt files for SR')
    args = parser.parse_args()

    if args.surface_realization_only:
        create_source_and_target_surface_realization_only(args)
    else:
        print('not doing anything yet')

if __name__ == '__main__':
    main()
