import argparse
import os
import pyconll
from tqdm import tqdm
from regex import Regex, UNICODE, IGNORECASE

def get_name_and_near(e2e_mr):
    # neither might be present
    xname = ''
    xnear = ''
    for act in e2e_mr:
        act_type = act[0:act.find('[')].strip()
        value = act[act.find('[')+1:act.find(']')]
        if act_type == 'name':
            xname = value
        elif act_type == 'near':
            xnear = value
    return xname, xnear

class Detokenizer(object):
    """\
    A simple de-tokenizer class.
    """

    def __init__(self):
        """\
        Constructor (pre-compile all needed regexes).
        """
        # compile regexes
        self._currency_or_init_punct = Regex(r' ([\p{Sc}\(\[\{\¿\¡]+) ', flags=UNICODE)
        self._noprespace_punct = Regex(r' ([\,\.\?\!\:\;\\\%\}\]\)]+) ', flags=UNICODE)
        self._contract = Regex(r" (\p{Alpha}+) ' (ll|ve|re|[dsmt])(?= )", flags=UNICODE | IGNORECASE)
        self._dash_fixes = Regex(r" (\p{Alpha}+|£ [0-9]+) - (priced|star|friendly|(?:£ )?[0-9]+) ", flags=UNICODE | IGNORECASE)
        self._dash_fixes2 = Regex(r" (non) - ([\p{Alpha}-]+) ", flags=UNICODE | IGNORECASE)
        self._international_things = {'chinese': 'Chinese', 'japanese':'Japanese',
                                      'french':'French', 'indian':'Indian',
                                      'english':'English', 'italian':'Italian'}

    def detokenize(self, text):
        """\
        Detokenize the given text.
        """
        text = ' ' + text + ' '
        text = self._dash_fixes.sub(r' \1-\2 ', text)
        text = self._dash_fixes2.sub(r' \1-\2 ', text)
        text = self._currency_or_init_punct.sub(r' \1', text)
        text = self._noprespace_punct.sub(r'\1 ', text)
        text = self._contract.sub(r" \1'\2", text)
        for word, capitalised_word in self._international_things.items():
            text = text.replace(word, capitalised_word)
        text = text.strip()
        # capitalize
        if not text:
            return ''
        text = text[0].upper() + text[1:]
        return text

def main():
    parser = argparse.ArgumentParser(description='''postprocess: relex, detok'''
                                     '''truecase the generate text''')
    # parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('-i', '--input_file_name', help='generated utterances')
    parser.add_argument('-m', '--mr_file_name', help='meaning representations')
    args = parser.parse_args()

    with open(args.input_file_name) as in_file:
        gen_utterances = [line.rstrip() for line in in_file]
    with open(args.mr_file_name) as in_file:
        meaning_reps = [line.rstrip().split(', ') for line in in_file]

    if len(gen_utterances) != len(meaning_reps):
        print("both input files need to be the same length!")
        return

    detok = Detokenizer()
    postprocessed_utterances = []
    for e2e_mr, utt in zip(meaning_reps, gen_utterances):
        xname, xnear = get_name_and_near(e2e_mr)
        relex_utterance = utt.replace('xname', xname)
        relex_utterance = relex_utterance.replace('Xnear', xnear)
        # TODO
        # Capitalise certain words like English, Japanese, etc.
        postprocessed_utt = detok.detokenize(relex_utterance)
        postprocessed_utterances.append(postprocessed_utt)

    output_file_name = os.path.join(args.input_file_name + '.postprocess')
    with open(output_file_name, 'w') as out_file:
        out_file.write('\n'.join(postprocessed_utterances))

if __name__ == '__main__':
    main()
