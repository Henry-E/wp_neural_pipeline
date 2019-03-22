# coding: utf8
from __future__ import unicode_literals

from pathlib import Path
import random
import sys 

import prodigy
from prodigy.core import recipe, recipe_args
from prodigy.components.printers import get_compare_printer
from prodigy.util import read_jsonl, log


@prodigy.recipe('compare',
        dataset=recipe_args['dataset'],
        a_file=("JSONL file for system responses", "positional", None, Path),
        b_file=("JSONL file for baseline responses", "positional", None, Path),
        no_random=("Don't randomise which annotation is shown as correct",
                   "flag", "NR", bool),
        diff=recipe_args['diff'],
        exclude=recipe_args['exclude'])
def compare(dataset, a_file, b_file, no_random=False, diff=False, exclude=None):
    """
    Compare output of two models and randomly assign A/B categories.
    """
    log("RECIPE: Starting recipe compare", locals())
    a_questions = read_jsonl(a_file)
    b_questions = read_jsonl(b_file)

    return {
        'dataset': dataset,
        'view_id': 'diff' if diff is True else 'compare',
        'stream': get_questions(a_questions, b_questions, not no_random, exclude),
        'update': None,
        'progress': None,
        'on_exit': get_compare_printer(Path(a_file).name, Path(b_file).name),
        'exclude': None,
    }


def get_questions(a_questions, b_questions, randomize, exclude=None):
    import ipdb; ipdb.set_trace()
    if exclude:
        with open(exclude[0]) as in_file:
            excluded_ids = [line.rstrip() for line in in_file]
    else:
        excluded_ids = []

    a_questions = {a['id']: a for a in a_questions}
    b_questions = {b['id']: b for b in b_questions}
    a_ids = list(a_questions.keys())
    random.shuffle(a_ids)
    for id_ in a_ids:
        a = a_questions[id_]
        if id_ not in b_questions or id_ in excluded_ids:
            continue
        question = {'id': id_, 'input': a['input']}
        a = a['output']
        b = b_questions[id_]['output']
        if a == b:
            continue
        if randomize and random.random() >= 0.5:
            question['input'] = {'text': '✅ {} \n ❌ {}'.format(b['text'], a['text'])}
            question['accept'], question['reject'] = b, a
            question['mapping'] = {'B': 'accept', 'A': 'reject'}
        else:
            if randomize:
                question['input'] = {'text': '✅ {} \n ❌ {}'.format(a['text'], b['text'])}
            question['accept'], question['reject'] = a, b
            question['mapping'] = {'A': 'accept', 'B': 'reject'}
        yield question
