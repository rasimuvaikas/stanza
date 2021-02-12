from hunspell import Hunspell
from stanza.models.pos.hunspeller.pos import *
from stanza.models.pos.hunspeller.decline import *


class Hunchecker():
    """
    Retrieve morphosyntactic information from a hunspell morphological analyser
    """

    def __init__(self, dict_file, dict_data_dir=None):
        self.h = Hunspell(dict_file, hunspell_data_dir=dict_data_dir)
        #h = Hunspell('lt-LT_morphology', hunspell_data_dir='D:/Hunspell-Zodynai-ir-gramatika-v.45')

    def hunspell_to_conll(self, input):
        """
        Retrieve morphosyntactic features of a single word
        :param input:  the word
        :return: a list of lists of possible lemmas (stems), UPOS, XPOS, and UFeats tags
        """

        all = {'Fem': 'mot', 'Masc': 'vyr', 'Neut': 'bev', 'Sg': 'vns', 'Pl': 'dgs', 'Nom': 'V', 'Gen': 'K', 'Dat': 'N',
               'Acc': 'G', 'Inst': 'Įn', 'Loc': 'Vt', 'Loc_short':'Vt', 'Voc': 'Š', 'Il': 'Il', 'Pres': 'es',
               'Past': 'būt-k', 'PastFreq': 'būt-d', 'Fut': 'būs', 'Indic': 'tiesiog', 'Subj': 'tar', 'Imper': 'liep',
               'Nec': 'reik', 'Pass': 'neveik', 'Act': 'veik', 'Part': 'dlv', 'Gerund': 'pad', 'HalfPart': 'pusd',
               'Inf': 'bndr', 'Vadv':'būdn', 'Def': 'įvardž', 'Comp': 'aukšt', 'Super': 'aukšč',
               'I': '1', 'II': '2', 'III': '3'}
        # PROPN, NOUN, VERB, ADJ, ADV, X, ADP, PART
        part_of_speech = {'noun_family_name': 'PROPN', 'noun_proper_name': 'PROPN', 'noun_first_name_substandard': 'PROPN',
               'noun_family_name_substandard': 'PROPN', 'noun_geographic_name': 'PROPN',
               'noun_geographic_name_obscene': 'PROPN', 'noun_proper_name_substandard': 'PROPN',
               'noun_first_name': 'PROPN', 'noun_reflexive': 'NOUN',
               'noun_reflexive_substandard': 'NOUN', 'noun': 'NOUN', 'noun_reflexive_obscene':'NOUN',
               'noun_substandard': 'NOUN', 'noun_obscene': 'NOUN', 'verb_reflexive_substandard':'VERB',
               'verb_reflexive_negative_substandard':'VERB', 'verb_reflexive': 'VERB', 'verb_reflexive_negative':'VERB',
               'verb': 'VERB', 'verb_substandard': 'VERB', 'verb_negative': 'VERB', 'verb_negative_substandard': 'VERB',
               'verb_obscene': 'VERB', 'verb_reflexive_obscene': 'VERB', 'verb_negative_obscene': 'VERB',
               'verb_reflexive_negative_obscene': 'VERB', 'adjective': 'ADJ', 'adjective_substandard': 'ADJ',
                'adjective_obscene': 'ADJ', 'adverb_obscene': 'ADV',
               'adverb': 'ADV', 'adverb_substandard': 'ADV', 'abbreviation_substandard': 'X', 'abbreviation_obscene': 'X',
               'abbreviation':'X', 'acronym':'X', 'acronym_substandard':'X',
                'preposition': 'ADP',
                'particle': 'PART'}

        sngr = ['noun_reflexive', 'noun_reflexive_substandard', 'noun_reflexive_obscene', 'verb_reflexive_substandard',
                'verb_reflexive_negative_substandard', 'verb_reflexive', 'verb_reflexive_negative',
                'verb_reflexive_obscene', 'verb_reflexive_negative_obscene']

        neig = ['verb_reflexive_negative_substandard', 'verb_reflexive_negative', 'verb_negative',
                'verb_negative_substandard', 'verb_negative_obscene', 'verb_reflexive_negative_obscene']

        sutr = ['abbreviation_substandard', 'abbreviation_obscene', 'abbreviation']

        akr = ['acronym', 'acronym_substandard']

        output = self.h.analyze(input)
        if len(output) < 1:
            return None, None, None, None
        poss_outputs = list()
        for o in output[::-1]:
            feats = set()
            for s in o.strip().split():
                if s.startswith('st:'):
                    stem = s[3:]
                elif s.startswith('po:'):
                    if s[3:].split('_')[0] == 'preposition':
                        pos = s[3:].split('_')[0]
                        feats.add(s[3:].split('_')[1])
                    else:
                        pos = s[3:]
                elif s.startswith('is:'):
                    for t in s[3:].split('_'):
                        feats.add(t)
            poss_outputs.append([stem, pos, feats])

        final_output = list()
        for p in poss_outputs:
            xpos = ''
            if p[1] in part_of_speech:
                po = part_of_speech[p[1]]
            else:
                continue
            for f in p[2]:
                if f in all:
                    if f == 'Past':
                        if 'Part' in p[2] and 'Pass' in p[2]:
                            xpos += 'būt.'
                        else:
                            xpos += all[f] + '.'
                    else:
                        xpos += all[f] + '.'
            if p[1] in sngr:
                xpos += 'sngr.'
            if p[1] in neig:
                xpos += 'neig.'
            if po == 'PART':
                features = '_'
                xpos = 'dll.'
            if po == 'ADP':
                p[2] = list(p[2])
                if p[2][0] == 'Inst':
                    p[2] = ['Ins'] 
                features = 'AdpType=Prep|Case=' + p[2][0]
                xpos = 'prl.' + xpos
            if po == 'X':
                features = 'Abbr=Yes'
                if p[1] in akr:
                    xpos = 'akr.'
                if p[1] in sutr:
                    xpos = 'sutr.'
            if po == 'PROPN' and len(p[2]) < 1: # naive assumption
                po = 'X'
                xpos = 'užs.'
                features = 'Foreign=Yes'
            if po == 'NOUN' or po == 'PROPN':
                xpos += 'dktv.'
                if po == 'PROPN':
                    xpos += 'tikr.'
                n = nominalise(input, stem, xpos)
                xpos = noun_to_xpos(n)
                features = xpos_to_feats(n)[1]
            if po == 'ADJ' or po == 'ADV':
                if 'Comp' not in p[2] and 'Super' not in p[2]:
                    xpos += 'nelygin.'
                if po == 'ADJ':
                    xpos += 'bdv.'
                    a = adjectivise(input, stem, xpos)
                    xpos = adj_to_xpos(a)
                    features = xpos_to_feats(a)[1]
                if po == 'ADV':
                    xpos += 'prv.'
                    a = adverbialise(input, stem, xpos)
                    xpos = adv_to_xpos(a)
                    features = xpos_to_feats(a)[1]
            if po == 'VERB':
                xpos2 = None
                if 'Supine' in p[2]:
                    continue
                xpos += 'vksm.'
                if 'Vadv' in p[2]:
                    xpos = 'vksm.' + 'neig.' if p[1] in neig else '' + 'būdn.'
                    features = 'Polarity=' + 'Pos' if p[1] not in neig else 'Neg' + '|VerbForm=Conv'
                    po = 'ADV'
                else:
                    if 'III' in p[2]:
                        xpos2 = xpos
                        xpos += 'vns.'
                        xpos2 += 'dgs.'
                    if 'Indic' in p[2] or 'Subj' in p[2] or 'Imper' in p[2]:
                        xpos += 'asm.'
                        if xpos2:
                            xpos2 += 'asm.'
                        
                    if xpos2:
                        v = verbalise(input, stem, xpos2)
                        xpos2 = verb_to_xpos(v)
                        features = xpos_to_feats(v)[1]
                        final_output.append([stem, po, xpos2, features])
                
                    
                    v = verbalise(input, stem, xpos)
                    xpos = verb_to_xpos(v)
                    features = xpos_to_feats(v)[1]

            final_output.append([stem, po, xpos, features])

        if len(final_output) < 1:
            return None, None, None, None

        else:
            lemma = [x[0] for x in final_output]
            upos = [x[1] for x in final_output]
            xpos = [x[2] for x in final_output]
            feats = [x[3] for x in final_output]
            return lemma, upos, xpos, feats
