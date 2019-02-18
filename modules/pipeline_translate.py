#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import configargparse
import copy
import csv
import os
import sys
import random
import logging

# opennmt imports
sys.path.insert(0, '/home/henrye/downloads/Henry_OpenNMT-py')
from onmt.utils.logging import init_logger
from onmt.translate.translator import build_translator

import onmt.opts as opts

# BERT imports
sys.path.insert(0, '/home/henrye/downloads/pytorch-pretrained-BERT')

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.distributed import DistributedSampler

from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
from pytorch_pretrained_bert.optimization import BertAdam, warmup_linear
from pytorch_pretrained_bert.file_utils import PYTORCH_PRETRAINED_BERT_CACHE

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

# BERT functions
class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.
        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label

class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids, label_id):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id

def convert_examples_to_features(examples, label_list, max_seq_length, tokenizer):
    """Loads a data file into a list of `InputBatch`s."""

    label_map = {label : i for i, label in enumerate(label_list)}

    features = []
    for (ex_index, example) in enumerate(examples):
        tokens_a = tokenizer.tokenize(example.text_a)

        tokens_b = None
        if example.text_b:
            tokens_b = tokenizer.tokenize(example.text_b)
            # Modifies `tokens_a` and `tokens_b` in place so that the total
            # length is less than the specified length.
            # Account for [CLS], [SEP], [SEP] with "- 3"
            _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        else:
            # Account for [CLS] and [SEP] with "- 2"
            if len(tokens_a) > max_seq_length - 2:
                tokens_a = tokens_a[:(max_seq_length - 2)]

        # The convention in BERT is:
        # (a) For sequence pairs:
        #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
        #  type_ids: 0   0  0    0    0     0       0 0    1  1  1  1   1 1
        # (b) For single sequences:
        #  tokens:   [CLS] the dog is hairy . [SEP]
        #  type_ids: 0   0   0   0  0     0 0
        #
        # Where "type_ids" are used to indicate whether this is the first
        # sequence or the second sequence. The embedding vectors for `type=0` and
        # `type=1` were learned during pre-training and are added to the wordpiece
        # embedding vector (and position vector). This is not *strictly* necessary
        # since the [SEP] token unambigiously separates the sequences, but it makes
        # it easier for the model to learn the concept of sequences.
        #
        # For classification tasks, the first vector (corresponding to [CLS]) is
        # used as as the "sentence vector". Note that this only makes sense because
        # the entire model is fine-tuned.
        tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
        segment_ids = [0] * len(tokens)

        if tokens_b:
            tokens += tokens_b + ["[SEP]"]
            segment_ids += [1] * (len(tokens_b) + 1)

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1] * len(input_ids)

        # Zero-pad up to the sequence length.
        padding = [0] * (max_seq_length - len(input_ids))
        input_ids += padding
        input_mask += padding
        segment_ids += padding

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length

        label_id = label_map[example.label]
        if ex_index < 5:
            pass
            # logger.info("*** Example ***")
            # logger.info("guid: %s" % (example.guid))
            # logger.info("tokens: %s" % " ".join(
            #         [str(x) for x in tokens]))
            # logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            # logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            # logger.info(
            #         "segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
            # logger.info("label: %s (id = %d)" % (example.label, label_id))

        features.append(
            InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_id=label_id))
    return features

def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""

    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()

def accuracy(out, labels):
    outputs = np.argmax(out, axis=1)
    return np.sum(outputs == labels)

def main(opt):
    # init the models / translators
    content_selection_opt = copy.deepcopy(opt)
    content_selection_opt.models = [opt.content_selection_model_file_name]
    content_selection_opt.beam_size = 1
    content_selection_opt.random_sampling_temp = 0.8
    content_selection_opt.random_sampling_topk = 10
    content_selection_translator = build_translator(content_selection_opt,
                                                    report_score=False)
    surface_realization_opt = copy.deepcopy(opt)
    surface_realization_opt.models = [opt.surface_realization_model_file_name]
    surface_realization_translator = build_translator(surface_realization_opt,
                                                      report_score=False)

    # Now we load bert model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = BertTokenizer.from_pretrained(
        opt.bert_model, do_lower_case=opt.do_lower_case)
    num_labels = 2
    model_state_dict = torch.load(opt.finetuned_bert_model_file_name)
    model = BertForSequenceClassification.from_pretrained(
        opt.bert_model, state_dict=model_state_dict, num_labels=num_labels)
    model.to(device)
    model.eval()

    # Load all the processed meaning representations
    with open(opt.tokenized_mr_file_name) as in_file:
        tokenized_mr_lines = [line.rstrip() for line in in_file]

    final_utterances = []
    for this_mr in tokenized_mr_lines:
        # TODO optionally skip these two and run with a single end-to-end model

        # content selection first
        duplicated_mr = [this_mr] * opt.num_hyps
        _, deep_utterance_hyps = content_selection_translator.translate(
            src=duplicated_mr,
            batch_size=opt.num_hyps)

        # we don't know what exactly the output from the translate function is
        # deep_utterance_hyps is a list of batchsize lists, of n_best
        # predictions. So we have a list of lists
        # TODO of course we could make this much more efficient eventually and
        # think of some way to batch together the sentences, but for now
        # keeping it simple
        utterance_hyps = []
        for this_deep_utterance in deep_utterance_hyps:
            this_utterance_sents = this_deep_utterance[0].split(' new_sent ')
            this_utterance_hyp = []
            for deep_sent in this_utterance_sents:
                _, out_sent = surface_realization_translator.translate(
                    src=[deep_sent],
                    batch_size=1)
                this_utterance_hyp.append(out_sent[0][0])
            utterance_hyps.append(' '.join(this_utterance_hyp))

        # Now for BERT!
        eval_examples = []
        for i, hyp in enumerate(utterance_hyps):
            # if i == 0:
            #     continue
            guid = "%s-%s" % ('hyps_to_test', i)
            text_a = this_mr
            text_b = hyp
            # TODO this might need to be a string rather than an int
            label = 'correct'
            eval_examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b,
                             label=label))

        # A lot of copypasta from existing implementation
        label_list = ['correct', 'wrong']
        eval_features = convert_examples_to_features(
            eval_examples, label_list, opt.max_seq_length, tokenizer)
        # logger.info("***** Running evaluation *****")
        # logger.info("  Num examples = %d", len(eval_examples))
        # logger.info("  Batch size = %d", args.eval_batch_size)
        all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
        all_label_ids = torch.tensor([f.label_id for f in eval_features], dtype=torch.long)
        eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
        # Run prediction for full data
        eval_sampler = SequentialSampler(eval_data)
        eval_dataloader = DataLoader(eval_data, sampler=eval_sampler,
                                     batch_size=opt.eval_batch_size)

        eval_loss, eval_accuracy = 0, 0
        nb_eval_steps, nb_eval_examples = 0, 0

        for input_ids, input_mask, segment_ids, label_ids in eval_dataloader:
            input_ids = input_ids.to(device)
            input_mask = input_mask.to(device)
            segment_ids = segment_ids.to(device)
            label_ids = label_ids.to(device)

            with torch.no_grad():
                tmp_eval_loss = model(input_ids, segment_ids, input_mask, label_ids)
                logits = model(input_ids, segment_ids, input_mask)
            # TODO
            # if there's more than 8 hypotheses we need to hang on to all the
            # logits and do topk on the later on
            _, indices = logits.topk(1)
        # TODO do the detokenization and relexicalization
        # Sorting temp
        logit_list = logits.cpu().tolist()
        logit_and_utterance = [this_logit + [this_utt] for this_logit,
                               this_utt in zip(logit_list, utterance_hyps)]
        utterances_sorted = sorted(logit_and_utterance,
                                   key=lambda hyps: hyps[0])
        import ipdb; ipdb.set_trace()
        #
        final_utterances.append(utterance_hyps[indices[0].item()])

    translator = build_translator(opt, report_score=True)
    translator.translate(
        src=opt.src,
        tgt=opt.tgt,
        src_dir=opt.src_dir,
        batch_size=opt.batch_size,
        attn_debug=opt.attn_debug
    )


if __name__ == "__main__":
    parser = configargparse.ArgumentParser(
        description='translate.py',
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    opts.config_opts(parser)
    opts.add_md_help_argument(parser)
    opts.translate_opts(parser)
    # Pipeline opts
    parser.add('--num_hyps', type=int, default=5,
               help='num of different utterance hypotheses to test')
    # models
    parser.add('--content_selection_model_file_name', type=str)
    parser.add('--surface_realization_model_file_name', type=str)
    parser.add('--finetuned_bert_model_file_name', type=str,
				help='needs to be a pytorch_model.bin file')
    # data
    parser.add('--devset_csv_file_name', type=str,
               default='/home/henrye/data/e2e-dataset/devset.csv')
    parser.add('--tokenized_mr_file_name', type=str,
               help='the tokenized and delexicalised meaning representations')
    # TODO output file name or directory
    # BERT opts
    parser.add('--bert_model', required=True, default=None, type=str,
                        help='Bert pre-trained model selected in the list: bert-base-uncased, '
                        'bert-large-uncased, bert-base-cased, bert-large-cased, bert-base-multilingual-uncased, '
                        'bert-base-multilingual-cased, bert-base-chinese.')
    parser.add('--do_lower_case',
                        action='store_true',
                        help='Set this flag if you are using an uncased model.')
    parser.add('--eval_batch_size',
                        default=8,
                        type=int,
                        help='Total batch size for eval.')
    parser.add('--max_seq_length',
                        default=128,
                        type=int,
                        help='The maximum total input sequence length after WordPiece tokenization. \n'
                             'Sequences longer than this will be truncated, and sequences shorter \n'
                             'than this will be padded.')

    opt = parser.parse_args()
    logger = init_logger(opt.log_file)
    main(opt)
