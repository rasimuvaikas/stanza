import mysql
from stanza.utils.conll import CoNLL as C
from stanza.models.common.doc import Document
from spacy.gold import align

import os

import numpy as np
from pandas import DataFrame as df

import hunspell as h
"""
Analyse tagger's errors
"""

UNIVERSAL_FEATURES = {
    "PronType", "NumType", "Poss", "Reflex", "Foreign", "Abbr", "Gender",
    "Animacy", "Number", "Case", "Definite", "Degree", "VerbForm", "Mood",
    "Tense", "Aspect", "Voice", "Evident", "Polarity", "Person", "Polite"
}


class Analyzer:

    def __init__(self, gold, pred, verbose=False, group=False):
        """
        Align golden and predicted tokens, and their tags. Create dictionaries of falsely predicted tags
        :param gold:  the gold conllu file
        :param pred: the predicted conlly file
        :param verbose: if true print information about token numbers
        :param group: if true, put falsely predicted ufeats labels into a dictionary that contains all the labels it was
        falsely assigned and the number of times each predicted label was found
        """

        gold = C.load_conll(open(gold,
                                 'r', encoding='utf8'))
        gold_dic = C.convert_conll(gold)  # returns a dictionary with all the column names
        gold_doc = Document(gold_dic)

        pred = C.load_conll(open(pred, 'r', encoding='utf8'))
        pred_dic = C.convert_conll(pred)  # returns a dictionary with all the column names
        pred_doc = Document(pred_dic)

        # get the tokens
        self.gold_tokens = [j['text'] for i in gold_dic for j in i]
        self.pred_tokens = [j['text'] for i in pred_dic for j in i]

        # get upos tags
        gold_tags = [j['upos'] for i in gold_dic for j in i]
        pred_tags = [j['upos'] for i in pred_dic for j in i]

        # get xpos tags
        gold_xpos = [j['xpos'] for i in gold_dic for j in i]
        pred_xpos = [j['xpos'] for i in pred_dic for j in i]

        # get ufeats tag
        gold_feats = list()
        pred_feats = list()
        for i in gold_dic:
            for j in i:
                if 'feats' in j:
                    gold_feats.append(j['feats'])
                else:
                    gold_feats.append('_')
        for i in pred_dic:
            for j in i:
                if 'feats' in j:
                    pred_feats.append(j['feats'])
                else:
                    pred_feats.append('_')

        if verbose:
            print('Number of gold tokens:', len(self.gold_tokens), ', number of predicted tokens:', len(self.pred_tokens))

        # align gold and predicted tokens
        cost, a2b, b2a, a2b_multi, b2a_multi = align(self.gold_tokens, self.pred_tokens)

        # align tokens and their POS tags separately
        self.aligned = list()  # tokens
        self.aligned_pos = list()  # upos
        self.aligned_feats = list()
        self.aligned_xpos = list()
        for i in range(len(b2a)):
            t = (self.gold_tokens[b2a[i]], self.pred_tokens[i])
            self.aligned.append(t)
            p = (gold_tags[b2a[i]], pred_tags[i])
            self.aligned_pos.append(p)
            f = (gold_feats[b2a[i]], pred_feats[i])
            self.aligned_feats.append(f)
            x = (gold_xpos[b2a[i]], pred_xpos[i])
            self.aligned_xpos.append(x)

        # align predicted tags to golden tags, not vice versa as before
        gold_aligned = list()
        for i in range(len(a2b)):
            t = (self.gold_tokens[i], self.pred_tokens[a2b[i]])
            gold_aligned.append(t)

        overall = list()
        for (a, b) in self.aligned:
            if a == b:
                overall.append((a, b))
        if verbose:
            print('Aligned tokens. GOLD:', len(gold_aligned), 'PREDICTED:', len(self.aligned), 'ALIGNED:', len(overall))

        self.conf_tags = {} # falsely predicted upos tags
        self.conf_tags_all = {}  # all upos tags
        self.incorrect_upos = 0  # number of incorrectly predicted upos tags
        # how many times different tags cooccured in gold and pred files
        i = 0
        for (a, b) in self.aligned_pos:
            if a != b:
                self.incorrect_upos += 1
                if (a, b) not in self.conf_tags:
                    self.conf_tags[(a, b)] = 1
                else:
                    self.conf_tags[(a, b)] += 1
            if (a, b) not in self.conf_tags_all:
                self.conf_tags_all[(a, b)] = 1
            else:
                self.conf_tags_all[(a, b)] += 1
            i += 1

        self.conf_feats = {}
        self.conf_feats_all = {}
        self.incorrect_feats = 0
        i = 0
        for (a, b) in self.aligned_feats:
            a = "|".join(sorted(feat for feat in a.split("|")
                                if feat.split("=", 1)[0] in UNIVERSAL_FEATURES))
            b = "|".join(sorted(feat for feat in b.split("|")
                                if feat.split("=", 1)[0] in UNIVERSAL_FEATURES))
            if a != b:
                self.incorrect_feats += 1
                # create a dictionary for each falsely predicted ufeats labels and group all its false predictions
                if group:
                    if a not in self.conf_feats:
                        self.conf_feats[a] = dict()
                        self.conf_feats[a][b] = 1
                    else:
                        if b not in self.conf_feats[a]:
                            self.conf_feats[a][b] = 1
                        else:
                            self.conf_feats[a][b] += 1
                else:
                    if (a, b) not in self.conf_feats:
                        self.conf_feats[(a, b)] = 1
                    else:
                        self.conf_feats[(a, b)] += 1
            if (a, b) not in self.conf_feats_all:
                self.conf_feats_all[(a, b)] = 1
            else:
                self.conf_feats_all[(a, b)] += 1
            i += 1

        self.conf_xpos = {}
        self.incorrect_xpos = 0
        i = 0
        for (a, b) in self.aligned_xpos:
            if a != b:
                self.incorrect_xpos += 1
                if (a, b) not in self.conf_xpos:
                    self.conf_xpos[(a, b)] = 1
                else:
                    self.conf_xpos[(a, b)] += 1
            i += 1

    def analyse_OOV(self, in_vocab):
        """
        Using vocab find which tokens do not belong to the vocabulary and are therefore OOV
        Calculate macro-averaged F1 scores for out of vocabulary words. Print statistical information.
        :param in_vocab: the vocabulary
        """
        vocab = set()
        with open(in_vocab, 'r', encoding='utf8') as r:
            for line in r:
                vocab.add(line.strip())


        gold_OOV = [g for g in self.gold_tokens if g not in vocab]
        pred_OOV = [p for p in self.pred_tokens if p not in vocab]
        print('OOV gold tokens:', len(gold_OOV), 'OOV predicted tokens:', len(pred_OOV))

        # find OOV error percentage
        incorrect_upos_OOV = 0
        i = 0
        for (a, b) in self.aligned_pos:
            if a != b:
                if self.aligned[i][0] not in vocab:
                    incorrect_upos_OOV += 1
            i += 1

        print('Incorrect OOV UPOS tags:', incorrect_upos_OOV, 'Number of correct tags:', len(pred_OOV) - incorrect_upos_OOV)
        print('Overall percentage of OOV UPOS tag errors:', incorrect_upos_OOV / self.incorrect_upos * 100 + '%')
        print('OOV UPOS tag F1 score:', 2 * (len(pred_OOV) - incorrect_upos_OOV) / (len(pred_OOV) + len(gold_OOV)) * 100 + '%')

        incorrect_feats_OOV = 0
        i = 0
        for (a, b) in self.aligned_feats:
            a = "|".join(sorted(feat for feat in a.split("|")
                                if feat.split("=", 1)[0] in UNIVERSAL_FEATURES))
            b = "|".join(sorted(feat for feat in b.split("|")
                                if feat.split("=", 1)[0] in UNIVERSAL_FEATURES))
            if a != b:
                self.incorrect_feats += 1
                if self.aligned[i][0] not in vocab:
                    incorrect_feats_OOV += 1
            i += 1

        print('Incorrect OOV UFeats tags:', incorrect_feats_OOV, 'Number of correct tags:', len(pred_OOV) - incorrect_feats_OOV)
        print('Overall percentage of OOV UFeats tag errors:', incorrect_feats_OOV / self.incorrect_feats * 100 + '%')
        print('OOV UFeats tag F1 score:', 2 * (len(pred_OOV) - incorrect_feats_OOV) / (len(pred_OOV) + len(gold_OOV)) * 100 + '%')

        incorrect_xpos_OOV = 0
        i = 0
        for (a, b) in self.aligned_xpos:
            if a != b:
                self.incorrect_xpos += 1
                if self.aligned[i][0] not in vocab:
                    incorrect_xpos_OOV += 1
            i += 1

        print('Incorrect OOV XPOS tags:', incorrect_xpos_OOV, 'Number of correct tags:', len(pred_OOV) - incorrect_xpos_OOV)
        print('Overall percentage of OOV XPOS tag errors:', incorrect_xpos_OOV / self.incorrect_xpos * 100)
        print('OOV XPOS tag F1 score:', 2 * (len(pred_OOV) - incorrect_xpos_OOV) / (len(pred_OOV) + len(gold_OOV)) * 100 + '%')

    def UPOS_matrix(self, upos=None, latex=True):
        """
        Print out UPOS confusion matrix.
        :param upos: a list with upos tags to appear in the matrix
        :param latex: if true, print the table in latex format
        """

        if upos is None:
            upos = ['VERB', 'NOUN', 'ADJ', 'PROPN', 'PRON', 'ADV', 'AUX']

        matrix = list()
        for p in upos:
            temp = list()
            for o in upos:
                if (p, o) in self.conf_tags_all:
                    temp.append(self.conf_tags_all[(p, o)])
                else:
                    temp.append(0)
            matrix.append(temp)

        print(matrix)
        print(np.array(matrix))
        if latex:
            print(df(np.array(matrix), columns=upos, index=upos).to_latex())

    def print_errors(self, upos=False, xpos=False, ufeats=False, outfile=None):

        """
        Print out lists of errors of different tags, in descending order of frequency
        :param upos: if true, print upos tag errors
        :param xpos: if true, print xpos tag errors
        :param ufeats: if true, print ufeats tag errors
        :param outfile: the file to print the errors into. if None, errors are printed on terminal line only
        """
        w = None
        if outfile:
            w = open(outfile, 'a', encoding='utf8')

        # print tag errors sorted by frequency
        def print_out(tag_type):
            if tag_type == 'upos':
                c = self.conf_tags
            elif tag_type == 'xpos':
                c = self.conf_xpos
            elif tag_type == 'ufeats':
                c = self.conf_feats

            errors = {k: v for k, v in sorted(c.items(), key=lambda item: item[1], reverse=True)}
            for e in errors:
                print(e, errors[e])
                if w:
                    w.write(a + '' + errors[e] + '\n')

        if upos:
            print('UPOS errors:')
            if w:
                w.write('\n' + 'UPOS errors:' + '\n')
            print_out('upos')

        if ufeats:
            print('UFeats errors:')
            if w:
                w.write('\n' + 'UFeats errors:' + '\n')
            print_out('ufeats')

        if xpos:
            print('XPOS errors:')
            if w:
                w.write('\n' + 'XPOS errors:' + '\n')
            print_out('xpos')
        if w:
            w.close()

    def analyse_error(self, tag_type, gold_tag, pred_tag, outfile=None):
        """
        Print out all occurrences of a particular tagging error, including the token and all its assigned tags
        :param tag_type: type of tag where the error occurred
        :param gold_tag:  the gold tag
        :param pred_tag: the falsely predicted tag
        :param outfile:  file to print errors into. if None, errors are printed into terminal only
        """

        if tag_type == 'upos':
            aligned = self.aligned_pos
        elif tag_type == 'xpos':
            aligned = self.aligned_xpos
        elif tag_type == 'ufeats':
            aligned = self.aligned_feats
        else:
            raise ValueError('Incorrect tag_type. Must be one of the following: "upos", "xpos", "ufeats".')

        w = None
        if outfile:
            w = open(outfile, 'a', encoding='utf8')

        i = 0
        if w:
            w.write('\n' + gold_tag + '\t' + pred_tag + ':' + '\n')
        for (a, b) in aligned:
            if tag_type == 'ufeats':
                a = "|".join(sorted(feat for feat in a.split("|")
                                    if feat.split("=", 1)[0] in UNIVERSAL_FEATURES))
                b = "|".join(sorted(feat for feat in b.split("|")
                                    if feat.split("=", 1)[0] in UNIVERSAL_FEATURES))
            if a == gold_tag and b == pred_tag:
                print(self.aligned[i], self.aligned_pos[i], self.aligned_xpos[i], self.aligned_feats[i])
                if w:
                    w.write(self.aligned[i] + ' ' + self.aligned_pos[i] + ' ' + self.aligned_xpos[i] + ' ' + self.aligned_feats[i] + '\n')
            i += 1


def compare(tag_type, comp_a:Analyzer, comp_b:Analyzer, print_errors=False):
    """
    Compare one predicted file with another (e.g. pre-filtered predictions vs. post-filtered predictions). Find out
    which and how many errors found in the first predicted file were corrected in the second one,
    which were retained, which were changed into another false tag, and what new errors the second file contains.
    print out the numbers of each category
    :param tag_type: type of tag to analyse prediction errors for
    :param comp_a: first prediction file
    :param comp_b: second prediction file
    :param print_errors: if true, print out the list of all errors
    """

    if tag_type == 'upos':
        pre = comp_a.aligned_pos
        post = comp_b.aligned_pos
    elif tag_type == 'xpos':
        pre = comp_a.aligned_xpos
        post = comp_b.aligned_xpos
    elif tag_type == 'ufeats':
        pre = comp_a.aligned_feats
        post = comp_b.aligned_feats

    all_errors = list()

    # Falsely predicted tags left behind:
    remaining = list()
    i = 0
    for (c, d) in pre:
        if c != d:
            if post[i][0] != post[i][1] and post[i][1] == d:
                remaining.append([[comp_a.aligned[i], comp_a.aligned_pos[i], comp_a.aligned_xpos[i],
                                   comp_a.aligned_feats[i]],
                                  [comp_b.aligned[i], comp_b.aligned_pos[i], comp_b.aligned_xpos[i],
                                   comp_b.aligned_feats[i]]])
        i += 1
    all_errors.append(remaining)

    # Corrected tags:
    corrected = list()
    i = 0
    for (c, d) in pre:
        if c != d:
            if post[i][0] == post[i][1]:
                corrected.append([[comp_a.aligned[i], comp_a.aligned_pos[i], comp_a.aligned_xpos[i],
                                   comp_a.aligned_feats[i]],
                                  [comp_b.aligned[i], comp_b.aligned_pos[i], comp_b.aligned_xpos[i],
                                   comp_b.aligned_feats[i]]])
        i += 1
    all_errors.append(corrected)

    # Falsely corrected tags:
    false_correct = list()
    i = 0
    for (c, d) in pre:
        if c != d:
            if post[i][0] != post[i][1] and post[i][1] != d:
                false_correct.append([[comp_a.aligned[i], comp_a.aligned_pos[i], comp_a.aligned_xpos[i],
                                       comp_a.aligned_feats[i]],
                                      [comp_b.aligned[i], comp_b.aligned_pos[i], comp_b.aligned_xpos[i],
                                       comp_b.aligned_feats[i]]])
        i += 1
    all_errors.append(false_correct)

    # New errors:
    new_incorrect = list()
    i = 0
    for (c, d) in pre:
        if c == d:
            if post[i][0] != post[i][1]:
                new_incorrect.append([[comp_a.aligned[i], comp_a.aligned_pos[i], comp_a.aligned_xpos[i],
                                       comp_a.aligned_feats[i]],
                                      [comp_b.aligned[i], comp_b.aligned_pos[i], comp_b.aligned_xpos[i],
                                       comp_b.aligned_feats[i]]])
        i += 1
    all_errors.append(new_incorrect)

    print('Number of remaining errors: ' + str(len(all_errors[0])))
    print('Number of corrected errors: ' + str(len(all_errors[1])))
    print('Number of falsely corrected errors: ' + str(len(all_errors[2])))
    print('Number of new errors: ' + str(len(all_errors[3])))

    if print_errors:
        for i in range(len(all_errors)):
            if i == 0:
                print('Remaining errors:')
            if i == 1:
                print('Corrected errors:')
            if i == 2:
                print('Falsely corrected errors:')
            if i == 3:
                print('New errors:')
            for a in all_errors[i]:
                print(a)


if __name__ == "__main__":

    ROOT = os.path.dirname(os.getcwd())

    a = Analyzer(ROOT + '/data_files/sme/sme_giella-ud-test.conllu',
                 ROOT + '/data_files/sme/baseline.parsed.conllu', group=True)

    b = Analyzer(ROOT + '/data_files/sme/sme_giella-ud-test.conllu',
                 ROOT + '/data_files/sme/post_filtered.parsed.conllu', group=True)

    ac = Analyzer(ROOT + '/data_files/lt/lt_alksnis-ud-test.conllu', ROOT + '/data_files/lt/baseline.parsed.conllu')

    bc = Analyzer(ROOT + '/data_files/lt/lt_alksnis-ud-test.conllu', ROOT + '/data_files/lt/post_filtered.parsed.conllu')

    ac.UPOS_matrix(latex=True)
    bc.UPOS_matrix(latex=True)

    compare('ufeats', a, b)







