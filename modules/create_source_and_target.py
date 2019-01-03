import argparse
import os
import re
import pyconll
import pyconll.tree

def process_deep_ud(deep_ud):
    linearized_deep = []
    for token in deep_ud:
        if token.form:
            linearized_deep.append(token.form)
    return linearized_deep

def main():
    parser = argparse.ArgumentParser(description='make the source files'
                                     ' readable')
    parser.add_argument('-o', '--output_dir_name', help='output directory')
    parser.add_argument('--sents_dir_name', help='source sents')
    parser.add_argument('--deep_ud_dir_name', help='deep ud conllu files')
    args = parser.parse_args()

    # regexes
    match_staart = re.compile(r"staart\w*")
    # we add exact matches for staart when using it later on to make devset
    match_exact_staart = re.compile(r"^staart\w*$")
    # match_sr_staart = re.compile(r"staart\w* start_deep_ud")
    match_end_of_story = re.compile(r"end_of_story")
    match_own_line_tokens = re.compile(r"(“|”|newwline|ennd\w*)")

    # TODO
    # We're starting to take a folder input approach, need to come up with a
    # canonical way to check that everything is ok with the input file names
    sents_file_root = os.listdir(args.sents_dir_name)[0]
    sents_file_name = os.path.join(args.sents_dir_name, sents_file_root)
    deep_ud_file_root = os.listdir(args.deep_ud_dir_name)[0]
    deep_ud_file_name = os.path.join(args.deep_ud_dir_name, deep_ud_file_root)

    with open(sents_file_name) as story_sentences:
        deep_uds = pyconll.iter_from_file(deep_ud_file_name)

        content_selection_src = []
        content_selection_tgt = []
        surface_realization_src = []
        surface_realization_tgt = []

        # we read it's much quicker to join a list of strings than keep a
        # continuously updating string https://waymoot.org/home/python_string/
        story_context_sents = []
        for sent, deep_ud in zip(story_sentences, deep_uds):
            sent = sent.strip()
            # don't try to predict story start tokens
            if match_staart.match(sent):
                story_context_sents.append(sent)
                continue
            content_selection_src.append(' '.join(story_context_sents))
            # TODO
            # this will be replaced with a processing function later
            deep_ud_processed = process_deep_ud(deep_ud)
            content_selection_tgt.append(' '.join(deep_ud_processed))
            # When it's the end of the story reset the context list
            if match_end_of_story.match(sent):
                story_context_sents = []
                continue
            # we don't try to predict single token sents
            if match_own_line_tokens.match(sent):
                story_context_sents.append(sent)
                continue
            surface_realization_src.append(' '.join(story_context_sents +
                                                    ['start_deep_ud'] +
                                                    deep_ud_processed))
            surface_realization_tgt.append(sent)
            story_context_sents.append(sent)

        dev_content_selection_src = []
        dev_content_selection_tgt = []
        dev_surface_realization_src = []
        dev_surface_realization_tgt = []

        # we're going with 30 stories because that gives us around 2,000 pairs
        # Have to run it twice because CS and SR have different lengths
        num_stories = 0
        while num_stories < 30:
            dev_content_selection_src.append(content_selection_src.pop())
            dev_content_selection_tgt.append(content_selection_tgt.pop())
            if match_exact_staart.match(dev_content_selection_src[-1]):
                num_stories += 1
        num_stories = 0
        while num_stories < 30:
            dev_surface_realization_src.append(surface_realization_src.pop())
            dev_surface_realization_tgt.append(surface_realization_tgt.pop())
            if surface_realization_src[-1].split('start_deep_ud')[0] not in \
                                            dev_surface_realization_src[-1]:
                num_stories += 1

        content_selection_dir_name = \
            os.path.join(args.output_dir_name, 'content_selection')
        os.makedirs(content_selection_dir_name, exist_ok=True)
        surface_realization_dir_name = \
            os.path.join(args.output_dir_name, 'surface_realization')
        os.makedirs(surface_realization_dir_name, exist_ok=True)
        input_file_root = os.path.splitext(deep_ud_file_root)[0]

        # got to do this eight times. Is there a cleaner way to do this?
        # Content selection first
        # Train
        # source
        train_src_file_name = os.path.join(content_selection_dir_name,
                                           input_file_root + '.train.src')
        with open(train_src_file_name, 'w') as out_file:
            out_file.write('\n'.join(content_selection_src))
        # target
        train_tgt_file_name = os.path.join(content_selection_dir_name,
                                           input_file_root + '.train.tgt')
        with open(train_tgt_file_name, 'w') as out_file:
            out_file.write('\n'.join(content_selection_tgt))
        # Dev
        # source
        dev_src_file_name = os.path.join(content_selection_dir_name,
                                         input_file_root + '.dev.src')
        with open(dev_src_file_name, 'w') as out_file:
            out_file.write('\n'.join(dev_content_selection_src))
        # target
        dev_tgt_file_name = os.path.join(content_selection_dir_name,
                                         input_file_root + '.dev.tgt')
        with open(dev_tgt_file_name, 'w') as out_file:
            out_file.write('\n'.join(dev_content_selection_tgt))
        # Surface realization next
        # Train
        # source
        train_src_file_name = os.path.join(surface_realization_dir_name,
                                           input_file_root + '.train.src')
        with open(train_src_file_name, 'w') as out_file:
            out_file.write('\n'.join(surface_realization_src))
        # target
        train_tgt_file_name = os.path.join(surface_realization_dir_name,
                                           input_file_root + '.train.tgt')
        with open(train_tgt_file_name, 'w') as out_file:
            out_file.write('\n'.join(surface_realization_tgt))
        # Dev
        # source
        dev_src_file_name = os.path.join(surface_realization_dir_name,
                                         input_file_root + '.dev.src')
        with open(dev_src_file_name, 'w') as out_file:
            out_file.write('\n'.join(dev_surface_realization_src))
        # target
        dev_tgt_file_name = os.path.join(surface_realization_dir_name,
                                         input_file_root + '.dev.tgt')
        with open(dev_tgt_file_name, 'w') as out_file:
            out_file.write('\n'.join(dev_surface_realization_tgt))

if __name__ == '__main__':
    main()
