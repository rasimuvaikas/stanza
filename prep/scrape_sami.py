import requests
from bs4 import BeautifulSoup


def get_pos(pos, word):
    """
    Retrieve the inflectional paradigm of a North Sami word through web scraping
    :param pos: part of speech the word belongs to
    :param word: the word to be searched
    :return: a tuple of lists containing every inflected form and its corresponding features
    """

    url = 'http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text=' + word + '%20&pos=' + pos + '&mode=full&action=paradigm&lang=sme&plang=eng'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # check if a paradigm is found
    table = soup.body
    if len(table.find_all('table')) < 2:
        if table.find_all('p')[2].text.strip() == 'No paradigm found':
            print('No paradigm found')
            return None, None

    all_feats = list()
    all_forms = list()

    table = soup.body.find_all('table')[1]
    paradigm = table.find_all('tr')
    for p in paradigm:
        td = p.find_all('td')
        feats = td[1].text.strip()
        form = td[2].text.strip()
        all_feats.append(feats)
        all_forms.append(form)
        if len(td) > 3:
            for t in td[3:]:
                all_feats.append(feats)
                all_forms.append(t.text.strip())

    return all_forms, all_feats


def sme_to_conllu(pos, line):
    """
    Transform giellatekno features format into the UD UFeats format used in conll-u files
    :param pos:  part of speech the word form belongs to
    :param line: a tab separated string: word form \t lemma \t features
    :return: a tuple containing a word form's UFeats and XPOS tags
    """

    convert = {'number': {'Sg': 'Sing', 'Pl': 'Plur', 'Du': 'Dual'},
               'cases': {'Nom': 'Nom', 'Gen': 'Gen', 'Acc': 'Acc', 'Loc': 'Loc', 'Ill': 'Ill', 'Ess': 'Ess',
                         'Com': 'Com', 'Abe': 'Abe'},
               'pron_type': {'Pers': 'Prs', 'Rel': 'Rel', 'Interr': 'Int', 'Dem': 'Dem', 'Indef': 'Ind',
                             'Recipr': 'Rcp', 'Refl': 'Prs|Reflex=Yes', 'Coll': 'Coll'},
               'degree': {'Comp': 'Cmp', 'Superl': 'Sup'},
               'mood': {'Cond': 'Cnd|VerbForm=Fin', 'Imprt': 'Imp|VerbForm=Fin', 'Ind': 'Ind|VerbForm=Fin',
                        'Pot': 'Pot|VerbForm=Fin'},
               'verb_form': {'Inf': 'Inf', 'Ger': 'Ger', 'VGen': 'Ger|Case=Gen', 'VAbess': 'Ger|Case=Abe',
                             'PrfPrc': 'Part|Aspect=Perf', 'PrsPrc': 'Part|Tense=Pres', 'Sup': 'Sup', 'Actio': 'Ger'},
               'num_per': {'Sg1': 'Number=Sing|Person=1', 'Sg2': 'Number=Sing|Person=2', 'Sg3': 'Number=Sing|Person=3',
                           'Du1': 'Number=Dual|Person=1', 'Du2': 'Number=Dual|Person=2', 'Du3': 'Number=Dual|Person=3',
                           'Pl1': 'Number=Plur|Person=1', 'Pl2': 'Number=Plur|Person=2', 'Pl3': 'Number=Plur|Person=3'},
               'tense': {'Prt': 'Past', 'Prs': 'Pres'},
               'voice': {'Der/PassL': 'Pass', 'Der/PassS': 'Pass'}
               }

    cardinals = ['nolla', 'nulla', 'okta', 'guokte', 'golbma', 'njeallje', 'vihtta', 'guhtta', 'čieža', 'gávcci',
                'ovcci', 'logi', 'oktanuppelohkái', 'guoktenuppelohkái', 'golbmanuppelohkái', 'njealljenuppelohkái',
                'vihttanuppelohkái', 'guhttanuppelohkái', 'čiežanuppelohkái',
                'gávccinuppelohkái', 'ovccinuppelohkái', 'guoktelogi', 'golbmalogi', 'njealljelogi', 'vihttalogi',
                'guhttalogi', 'čiežalogi', 'gávccilogi', 'ovccilogi', 'guoktelot', 'golbmalot', 'njealljelot',
                'vihttalot', 'guhttalot', 'čiežalot', 'gávccilot', 'ovccilot', 'čuođi', 'golbmačuođi', 'njeallječuođi',
                'vihttačuođi', 'guhttačuođi', 'čiežačuođi', 'gávccičuođi', 'ovccičuođi', 'duhát', 'guokteduhát',
                'golbmaduhát', 'njealljeduhát', 'millijovdna', 'miljon', 'beannot']

    feats = list()

    line = line.split('\t')
    l = line[2].split()

    if pos == 'Num':
        if line[1] in cardinals or (line[1].endswith('okta') or line[1].endswith('guokte') or
                                    line[1].endswith('golbma') or line[1].endswith('njeallje') or
                                    line[1].endswith('vihtta') or line[1].endswith('guhtta') or
                                    line[1].endswith('čieža') or line[1].endswith('gávcci') or
                                    line[1].endswith('ovcci')) or line[1].isdigit():
            feats.append('NumType=Card')

    if pos == 'N':
        # find compounds
        temp = [l.index(x) for x in l if 'Cmp#' in x]
        cmp = None
        if len(temp) > 0:
            cmp = temp[-1]
        # relevant compound info is at the end
        if cmp:
            l = l[cmp+1:]

    psor = ['Px' in x for x in l]
    index = None
    if True in psor: # possessive suffix found
        index = psor.index(True)
    if index:
        feats.append('Number[psor]=' + convert['number'][l[index][2:4]])
        feats.append('Person[psor]=' + l[index][4])
    for i in l:
        if i in convert['number']:
            feats.append('Number=' + convert['number'][i])
        elif i in convert['cases']:
            feats.append('Case=' + convert['cases'][i])
        elif i in ['1', '2', '3']:
            feats.append('Person=' + i)
        elif i in convert['pron_type']:
            feats.append('PronType=' + convert['pron_type'][i])
        elif i in convert['mood']:
            feats.append('Mood=' + convert['mood'][i])
        elif i in convert['verb_form']:
            feats.append('VerbForm=' + convert['verb_form'][i])
        elif i in convert['num_per']:
            feats.append(convert['num_per'][i])
        elif i in convert['tense']:
            feats.append('Tense=' + convert['tense'][i])
        elif i in convert['voice']:
            feats.append('Voice=' + convert['voice'][i])
        elif i == 'ConNeg':
            feats.append('Connegative=Yes')
        elif i == 'Neg':
            feats.append('Polarity=Neg')

    if pos == 'Adv' or pos == 'A':
        for i in l:
            if i in convert['degree']:
                feats.append('Degree=' + convert['degree'][i])

    if len(feats) < 1:
        return '_', pos
    feats = '|'.join(sorted(feats))
    # sort alphabetically
    feats_temp = [i.split('=') for i in feats.split('|')]
    feats = '|'.join([i[0] + '=' + i[1] for i in sorted(feats_temp)])

    return feats, pos