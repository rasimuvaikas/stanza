# Classes for the different POS

class Noun:
    def __init__(self, word, lemma, gender, number=None, infl=None, proper=False, rflx=False):
        self.word = word
        self.rflx = rflx
        self.lemma = lemma
        self.proper = proper
        self.gender = gender
        self.number = number
        self.infl = infl


class Verb:
    def __init__(self, word, lemma, verb_form, number=None, tense=None, person=None, mood=None,
                gender=None, infl=None, rflx=False,
                 polarity='teig', defin=None, voice=None):
        self.verb_form = verb_form
        self.polarity = polarity
        self.rflx = rflx
        self.mood = mood
        self.word = word
        self.lemma = lemma
        self.voice = voice
        self.tense = tense
        self.definite = defin
        self.gender = gender
        self.number = number
        self.person = person
        self.infl = infl


    def __eq__(self, other):
        """Compare two verb objects

        :param other: the other verb object
        :return: True if the two verbs are the same
        """
        if not isinstance(other, Verb):
            return False

        return (self.word.lower() == other.word.lower()
        and self.lemma == other.lemma
        and self.number == other.number
        and self.tense == other.tense
        and self.person == other.person
        and self.mood == other.mood
        and self.verb_form == other.verb_form
        and self.rflx == other.rflx
        and self.gender == other.gender
        and self.infl == other.infl
        and self.polarity == other.polarity
        and self.definite == other.definite
        and self.voice == other.voice)

    def __copy__(self):
        """Shallow copy a verb object

        :return: a new Verb object
        """

        return Verb(self.word.lower(), self.lemma, self.verb_form,
                    self.number, self.tense, self.person,
                    self.mood, self.gender, self.infl, self.rflx, self.polarity, self.definite, self.voice)


class Adjective:
    def __init__(self, word, lemma, gender=None, degree=None, number=None, infl=None, dfnt=False):
        self.word = word
        self.lemma = lemma
        self.gender = gender
        self.number = number
        self.infl = infl
        self.dfnt = dfnt
        self.degree = degree


class Pronoun:
    def __init__(self, word, lemma, gender, number, infl):
        self.word = word
        self.lemma = lemma
        self.gender = gender
        self.number = number
        self.infl = infl


class Numeral:
    def __init__(self, word, lemma, num_form, num_type, gender=None, number=None, infl=None, dfnt=False, degree=None):
        self.word = word
        self.lemma = lemma
        self.num_form = num_form
        self.num_type = num_type
        self.gender = gender
        self.number = number
        self.infl = infl
        self.dfnt = dfnt
        self.degree = degree


class Adverb:

    def __init__(self, word, lemma, degree='nelygin', pron_type=None):
        self.word = word
        self.lemma = lemma
        self.degree = degree
        self.pron_type = pron_type


def verbalise(verb, lemma, info):
    """Verbalise Lithuanian info -> create a Verb object

    :param verb: the inflected verb form
    :param lemma: the verb lemma
    :param info: Lithuanian xpos data
    :return: a Verb object
    """

    all = {'gender': ['mot', 'vyr', 'bev'], 'number': ['vns', 'dgs'], 'infl': ['V', 'K', 'N', 'G', 'Įn', 'Vt', 'Š', 'Il'],
           'person': ['1', '2', '3'], 'tense': ['es', 'būt-k', 'būt-d', 'būs', 'būt'], 'mood': ['tiesiog', 'tar', 'liep', 'reik'],
           'voice': ['neveik', 'veik'], 'verb_form': ['asm', 'dlv', 'pad', 'pusd', 'bndr', 'padlv', 'būdn']}

    xpos = info.strip('.').split('.')

    args = dict()
    args['word'] = verb
    args['lemma'] = lemma

    for x in xpos:
        for a in all.keys():
            if x in all[a]:
                args[a] = x

    if 'neig' in xpos:
        args['polarity']='neig'

    if 'sngr' in xpos:
        args['rflx'] = True

    if 'įvardž' in xpos:
        args['defin'] = 'įvardž'
    elif args['verb_form'] == 'dlv':
        args['defin'] = 'neįvardž'

    return Verb(**args)


def nominalise(noun, lemma, info):
    """Nominalise Lithuanian info -> create a Noun object

    :param noun: the inflected noun form
    :param lemma: the noun lemma
    :param info: Lithuanian xpos data
    :return: a Noun object
    """

    all = {'gender': ['mot', 'vyr', 'bev'], 'number': ['vns', 'dgs'], 'infl': ['V', 'K', 'N', 'G', 'Įn', 'Vt', 'Š', 'Il']}

    xpos = info.strip('.').split('.')

    args = dict()
    args['word'] = noun
    args['lemma'] = lemma

    if 'tikr' in xpos:
        args['proper'] = True

    for x in xpos:
        for a in all.keys():
            if x in all[a]:
                args[a] = x

    if 'sngr' in xpos:
        args['rflx'] = True

    return Noun(**args)


def adjectivise(adj, lemma, info):
    """Adjectivise Lithuanian info -> create an Adjective object

    :param verb: the inflected adjective form
    :param lemma: the adjective lemma
    :param info: Lithuanian xpos data
    :return: an Adjective object
    """

    all = {'gender': ['mot', 'vyr', 'bev'], 'number': ['vns', 'dgs'], 'infl': ['V', 'K', 'N', 'G', 'Įn', 'Vt', 'Il'],
           'degree': ['nelygin', 'aukšt', 'aukšč']}

    xpos = info.strip('.').split('.')

    args = dict()
    args['word'] = adj
    args['lemma'] = lemma

    for x in xpos:
        for a in all.keys():
            if x in all[a]:
                args[a] = x

    if 'įvardž' in xpos:
        args['dfnt'] = True

    return Adjective(**args)


def numeralise(numeral, lemma, info):
    """Numeralise Lithuanian info -> create a Numeral object

    :param verb: the inflected numeral form
    :param lemma: the numeral lemma
    :param info: Lithuanian xpos data
    :return: a Numeral object
    """

    all = {'gender': ['mot', 'vyr', 'bev'], 'number': ['vns', 'dgs'], 'infl': ['V', 'K', 'N', 'G', 'Įn', 'Vt', 'Il'],
           'degree': ['nelygin', 'aukšt', 'aukšč'], 'num_form': ['arab', 'rom', 'mišr', 'raid'],
           'num_type': ['kiek', 'kelint', 'daugin', 'kuopin', 'trup']} # added trup myself, jablonskis tagset used in conllu doesnt have name for fraction

    xpos = info.strip('.').split('.')

    args = dict()
    args['word'] = numeral
    args['lemma'] = lemma

    for x in xpos:
        for a in all.keys():
            if x in all[a]:
                args[a] = x

    if 'įvardž' in xpos:
        args['dfnt'] = True

    if 'aukšt' in xpos:
        args['degree'] = 'aukšt'
    elif 'aukšč' in xpos:
        args['degree'] = 'aukšč'
    elif lemma == 'pirmas':
        args['degree'] = 'nelygin'

    return Numeral(**args)


def adverbialise(adverb, lemma, info):
    """Adverbialise Lithuanian info -> create an Adverb object

    :param verb: the adverb form
    :param lemma: the adverb lemma
    :param info: Lithuanian xpos data
    :return: an Adverb object
    """

    all = {'degree': ['nelygin', 'aukšt', 'aukšč']}

    xpos = info.strip('.').split('.')

    args = dict()
    args['word'] = adverb
    args['lemma'] = lemma

    for x in xpos:
        for a in all.keys():
            if x in all[a]:
                args[a] = x

    return Adverb(**args)
