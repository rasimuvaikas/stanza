from stanza.models.pos.hunspeller.pos import Verb, Noun, Pronoun, Adjective, Numeral, Adverb, numeralise

# Decline numerals and convert other pos features into XPOS and UFeats formats

def decline_num(num, rqrd_infl, rqrd_num=None, rqrd_gen=None):
    """Decline numerals

    :param num: Numeral object
    :param rqrd_infl: the inflection the numeral should be inflected for
    :param rqrd_num: the number the numeral should be inflected for
    :param rqrd_gen: the gender the numeral should be inflected for
    :return: a Numeral object with the numeral in a desired form and its grammatical information
    """

    lemma = num.lemma
    word = None

    number = num.number
    gender = num.gender
    num_type = num.num_type

    if num_type == 'kiek' and number is None and gender is None:
        # cardinal numbers / simple numerals from 11 to 19 are not inflected for gender
        if rqrd_infl == 'V':
            if lemma.endswith('lika'):
                word = lemma
        if rqrd_infl == 'K':
            if lemma.endswith('lika'):
                word = lemma[0:len(lemma) - 1] + 'os'
        if rqrd_infl == 'N':
            if lemma.endswith('lika'):
                word = lemma[0:len(lemma) - 1] + 'ai'
        if rqrd_infl == 'G':
            if lemma.endswith('lika'):
                word = lemma[0:len(lemma) - 1] + 'ą'
        if rqrd_infl == 'Įn':
            if lemma.endswith('lika'):
                word = lemma[0:len(lemma) - 1] + 'a'
        if rqrd_infl == 'Vt':
            if lemma.endswith('lika'):
                word = lemma[0:len(lemma) - 1] + 'oje'

    elif number is None and gender is not None:
        # cardinal numbers / simple numerals from 1 to 10 inflected for gender and cardinal plurals
        if rqrd_gen == 'vyr':
            if rqrd_infl == 'V':
                if lemma == 'du':
                    word = lemma
                elif lemma == 'trys':
                    word = lemma
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma
                elif lemma.endswith('lika'):
                    word = lemma
                elif lemma.endswith('eji'):
                    word = lemma
                elif lemma.endswith('eri'):
                    word = lemma
            if rqrd_infl == 'K':
                if lemma == 'du':
                    word = 'dviejų'
                elif lemma == 'trys':
                    word = 'trijų'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'ų'
                elif lemma.endswith('lika'):
                    word = lemma[0:len(lemma)-1] + 'os'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'ų'
                elif lemma.endswith('eri'):
                    word = lemma + 'ų'
            if rqrd_infl == 'N':
                if lemma == 'du':
                    word = 'dviem'
                elif lemma == 'trys':
                    word = 'trims'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'ems'
                elif lemma.endswith('lika'):
                    word = lemma[0:len(lemma)-1] + 'ai'
                elif lemma.endswith('eji'):
                    word = lemma + 'ems'
                elif lemma.endswith('eri'):
                    word = lemma + 'ems'
            if rqrd_infl == 'G':
                if lemma == 'du':
                    word = 'du'
                elif lemma == 'trys':
                    word = 'tris'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 's'
                elif lemma.endswith('lika'):
                    word = lemma[0:len(lemma)-1] + 'ą'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'us'
                elif lemma.endswith('eri'):
                    word = lemma + 'us'
            if rqrd_infl == 'Įn':
                if lemma == 'du':
                    word = 'dviem'
                elif lemma == 'trys':
                    word = 'trimis'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'ais'
                elif lemma.endswith('lika'):
                    word = lemma[0:len(lemma)-1] + 'a'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'ais'
                elif lemma.endswith('eri'):
                    word = lemma + 'ais'
            if rqrd_infl == 'Vt':
                if lemma == 'du':
                    word = 'dviejuose'
                elif lemma == 'trys':
                    word = 'trijuose'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'uose'
                elif lemma.endswith('lika'):
                    word = lemma[0:len(lemma)-1] + 'oje'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'uose'
                elif lemma.endswith('eri'):
                    word = lemma + 'uose'
        else:  # feminine gender
            if rqrd_infl == 'V':
                if lemma == 'du':
                    word = 'dvi'
                elif lemma == 'trys':
                    word = 'trys'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'os'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'os'
                elif lemma.endswith('eri'):
                    word = lemma + 'os'
            if rqrd_infl == 'K':
                if lemma == 'du':
                    word = 'dviejų'
                elif lemma == 'trys':
                    word = 'trijų'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'ų'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'ų'
                elif lemma.endswith('eri'):
                    word = lemma + 'ų'
            if rqrd_infl == 'N':
                if lemma == 'du':
                    word = 'dviem'
                elif lemma == 'trys':
                    word = 'trim'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'oms'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'oms'
                elif lemma.endswith('eri'):
                    word = lemma + 'oms'
            if rqrd_infl == 'G':
                if lemma == 'du':
                    word = 'dvi'
                elif lemma == 'trys':
                    word = 'tris'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'as'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'as'
                elif lemma.endswith('eri'):
                    word = lemma + 'as'
            if rqrd_infl == 'Įn':
                if lemma == 'du':
                    word = 'dviem'
                elif lemma == 'trys':
                    word = 'trimis'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'omis'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'omis'
                elif lemma.endswith('eri'):
                    word = lemma + 'omis'
            if rqrd_infl == 'Vt':
                if lemma == 'du':
                    word = 'dviejose'
                elif lemma == 'trys':
                    word = 'trijose'
                elif lemma == 'keturi' or lemma == 'penki' or lemma == 'šeši' or lemma == 'septyni' \
                        or lemma == 'aštuoni' or lemma == 'devyni':
                    word = lemma + 'ose'
                elif lemma.endswith('eji'):
                    word = lemma[:-1] + 'ose'
                elif lemma.endswith('eri'):
                    word = lemma + 'ose'

    elif rqrd_num == 'vns' or rqrd_num is None:
        if rqrd_gen == 'vyr' or (rqrd_gen is None and num.gender != 'mot'):
            if rqrd_infl == 'V':
                if lemma == 'vienas':
                    word = lemma
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausias'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnis'
                    else:
                        word = lemma
                elif lemma == 'tūkstantis':
                    word = lemma
                elif lemma.endswith('is'):
                    word = lemma
            if rqrd_infl == 'K':
                if lemma == 'vienas':
                    word = 'vieno'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausio'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnio'
                    else:
                        word = lemma[:-2] + 'o'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čio'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'io'
            if rqrd_infl == 'N':
                if lemma == 'vienas':
                    word = 'vienam'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('etas') or (num.num_type == 'kiek'
                        and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    word = lemma[:-2] + 'ui'
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiam'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esniam'
                    else:
                        word = lemma[:-2] + 'am'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čiui'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'iam'
            if rqrd_infl == 'G':
                if lemma == 'vienas':
                    word = 'vieną'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausią'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnį'
                    else:
                        word = lemma[:-2] + 'ą'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'tį'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'į'
            if rqrd_infl == 'Įn':
                if lemma == 'vienas':
                    word = 'vienu'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiu'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esniu'
                    else:
                        word = lemma[:-2] + 'u'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čiu'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'iu'
            if rqrd_infl == 'Vt':
                if lemma == 'vienas':
                    word = 'viename'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('etas') or (num.num_type == 'kiek'
                        and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    word = lemma[:-2] + 'e'
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiame'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esniame'
                    else:
                        word = lemma[:-2] + 'ame'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'tyje'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'iame'
        else:  # feminine gender
            if rqrd_infl == 'V' or (rqrd_gen is None and num.gender == 'mot'):
                if lemma == 'vienas':
                    word = 'viena'
                elif lemma.endswith('dešimtis'):
                    word = lemma
                elif lemma.endswith('etas') or \
                        (num.num_type == 'kiek'
                         and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausia'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnė'
                    else:
                        word = lemma[:-2] + 'a'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ė'
            if rqrd_infl == 'K':
                if lemma == 'vienas':
                    word = 'vienos'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'ies'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausios'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnės'
                    else:
                        word = lemma[:-2] + 'os'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ės'
            if rqrd_infl == 'N':
                if lemma == 'vienas':
                    word = 'vienai'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-3] + 'čiai'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiai'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnei'
                    else:
                        word = lemma[:-2] + 'ai'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ei'
            if rqrd_infl == 'G':
                if lemma == 'vienas':
                    word = 'vieną'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'į'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausią'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnę'
                    else:
                        word = lemma[:-2] + 'ą'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ę'
            if rqrd_infl == 'Įn':
                if lemma == 'vienas':
                    word = 'viena'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'imi'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausia'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esne'
                    else:
                        word = lemma[:-2] + 'a'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'e'
            if rqrd_infl == 'Vt':
                if lemma == 'vienas':
                    word = 'vienoje'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'yje'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausioje'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnėje'
                    else:
                        word = lemma[:-2] + 'oje'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ėje'
    else:  # rqrd plural
        if rqrd_gen == 'vyr' or (rqrd_gen is None and num.gender != 'mot'):
            if rqrd_infl == 'V':
                if lemma == 'vienas':
                    word = 'vieni'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    word = lemma[:-2] + 'ai'
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausi'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esni'
                    else:
                        word = lemma[:-2] + 'i'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čiai'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'i'
            if rqrd_infl == 'K':
                if lemma == 'vienas':
                    word = 'vienų'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('etas') or lemma == 'šimtas' \
                        or lemma == 'milijonas' or lemma == 'milijardas' or lemma == 'ketvertas':
                    word = lemma[:-2] + 'ų'
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausių'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnių'
                    else:
                        word = lemma[:-2] + 'ų'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čių'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ių'
            if rqrd_infl == 'N':
                if lemma == 'vienas':
                    word = 'vieniems'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    word = lemma[:-2] + 'ams'
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiems'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esniems'
                    else:
                        word = lemma[:-2] + 'iems'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čiams'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'iems'
            if rqrd_infl == 'G':
                if lemma == 'vienas':
                    word = 'vienus'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('etas') or lemma == 'šimtas' \
                        or lemma == 'milijonas' or lemma == 'milijardas' or lemma == 'ketvertas':
                    word = lemma[:-2] + 'us'
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausius'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnius'
                    else:
                        word = lemma[:-2] + 'us'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čius'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ius'
            if rqrd_infl == 'Įn':
                if lemma == 'vienas':
                    word = 'vienais'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('etas') or lemma == 'šimtas' \
                        or lemma == 'milijonas' or lemma == 'milijardas' or lemma == 'ketvertas':
                    word = lemma[:-2] + 'ais'
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiais'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esniais'
                    else:
                        word = lemma[:-2] + 'ais'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čiais'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'iais'
            if rqrd_infl == 'Vt':
                if lemma == 'vienas':
                    word = 'vienuose'
                elif lemma.endswith('dešimtis'):
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiuose'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esniuose'
                    else:
                        word = lemma[:-2] + 'uose'
                elif lemma == 'tūkstantis':
                    word = lemma[:-3] + 'čiuose'
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'iuose'
        else:  # feminine gender
            if rqrd_infl == 'V':
                if lemma == 'vienas':
                    word = 'vienos'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'ys'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausios'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnės'
                    else:
                        word = lemma[:-2] + 'os'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ės'
            if rqrd_infl == 'K':
                if lemma == 'vienas':
                    word = 'vienų'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-3] + 'čių'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausių'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnių'
                    else:
                        word = lemma[:-2] + 'ų'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ių'
            if rqrd_infl == 'N':
                if lemma == 'vienas':
                    word = 'vienoms'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'ims'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausioms'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnėms'
                    else:
                        word = lemma[:-2] + 'oms'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ėms'
            if rqrd_infl == 'G':
                if lemma == 'vienas':
                    word = 'vienas'
                elif lemma.endswith('dešimtis'):
                    word = lemma
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausias'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnes'
                    else:
                        word = lemma[:-2] + 'as'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'es'
            if rqrd_infl == 'Įn':
                if lemma == 'vienas':
                    word = 'vienomis'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'imis'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiomis'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnėmis'
                    else:
                        word = lemma[:-2] + 'omis'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ėmis'
            if rqrd_infl == 'Vt':
                if lemma == 'vienas':
                    word = 'vienose'
                elif lemma.endswith('dešimtis'):
                    word = lemma[:-2] + 'yse'
                elif lemma.endswith('etas') \
                        or (num.num_type == 'kiek'
                            and (lemma == 'šimtas' or lemma == 'milijonas' or lemma == 'milijardas')) \
                        or lemma == 'ketvertas':
                    return
                elif lemma.endswith('as'):
                    if num.degree == 'aukšč':
                        word = lemma[:-2] + 'iausiose'
                    elif num.degree == 'aukšt':
                        word = lemma[:-2] + 'esnėse'
                    else:
                        word = lemma[:-2] + 'ose'
                elif lemma == 'tūkstantis':
                    return
                elif lemma.endswith('is'):
                    word = lemma[:-2] + 'ėse'

    if word is None:
        return
    else:
        if rqrd_gen is not None and rqrd_num is not None and rqrd_infl is not None:
            n = Numeral(word, lemma, num.num_form, num.num_type, rqrd_gen, rqrd_num, rqrd_infl, num.dfnt, degree=num.degree)
        elif rqrd_gen is not None and rqrd_infl is not None:
            n = Numeral(word, lemma, num.num_form, num.num_type, rqrd_gen, infl=rqrd_infl, number=num.number, dfnt=num.dfnt, degree=num.degree)
        elif rqrd_num is not None and rqrd_infl is not None:
            n = Numeral(word, lemma, num.num_form, num.num_type, gender=num.gender, number=rqrd_num, infl=rqrd_infl, degree=num.degree)
        elif rqrd_infl is not None:
            n = Numeral(word, lemma, num.num_form, num.num_type, gender=num.gender, number=num.number, infl=rqrd_infl, degree=num.degree)
        else:
            n = Numeral(word, lemma, num.num_form, num.num_type, gender=num.gender, number=num.number, infl=num.infl, degree=num.degree)

    return n


def num_def(num, rqrd_gen, rqrd_num=None, rqrd_infl=None):
    """Decline definite numerals. Only possible with ordinal numerals

    :param num: Numeral object
    :param rqrd_gen: the gender the numeral should be inflected for
    :param rqrd_num: the number the numeral should be inflected for
    :param rqrd_infl: the inflection the numeral should be inflected for
    :return: a Numeral object with the numeral in a desired form and its grammatical information
    """

    real_lemma = num.lemma
    lemma = num.lemma
    # only ordinal numerals can be definite
    if num.degree is None or num.degree == 'nelygin' or num.degree == 'aukšč':
        if num.degree == 'aukšč':
            lemma = lemma[:-2] + 'iausias'
        if rqrd_num == 'vns':
            if rqrd_gen == 'vyr':
                if rqrd_infl == 'V':
                    word = lemma + 'is'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'ojo'
                elif rqrd_infl == 'N':
                    word = lemma[:-2] + 'ajam'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'ąjį'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'uoju'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'ajame'
            elif rqrd_gen == 'mot':  # neuter or fem
                if rqrd_infl == 'V':
                    word = lemma[:-2] + 'oji'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'osios'
                elif rqrd_infl == 'N':
                    word = lemma[:-2] + 'ajai'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'ąją'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'ąja'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'ojoje'
        else:  # plural num
            if rqrd_gen == 'vyr':
                if rqrd_infl == 'V':
                    if lemma.endswith('ias'):
                        word = lemma[:-2] + 'eji'
                    else:
                        word = lemma[:-2] + 'ieji'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'ųjų'
                elif rqrd_infl == 'N':
                    if lemma.endswith('ias'):
                        word = lemma[:-2] + 'esiems'
                    else:
                        word = lemma[:-2] + 'iesiems'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'uosius'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'aisiais'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'uosiuose'
            elif rqrd_gen == 'mot':  # neuter or fem
                if rqrd_infl == 'V':
                    word = lemma[:-2] + 'osios'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'ųjų'
                elif rqrd_infl == 'N':
                    word = lemma[:-2] + 'osioms'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'ąsias'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'osiomis'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'osiose'
    else:
        lemma = lemma[:-2] + 'esnis'
        if rqrd_num == 'vns':
            if rqrd_gen == 'vyr':
                if rqrd_infl == 'V':
                    word = lemma[:-2] + 'ysis'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'iojo'
                elif rqrd_infl == 'N':
                    word = lemma[:-2] + 'iajam'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'įjį'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'iuoju'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'iajame'
            elif rqrd_gen == 'mot':  # neuter or fem
                if rqrd_infl == 'V':
                    word = lemma[:-2] + 'ioji'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'iosios'
                elif rqrd_infl == 'N':
                    word = lemma[:-2] + 'iajai'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'iąją'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'iąja'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'iojoje'
        else:  # plural num
            if rqrd_gen == 'vyr':
                if rqrd_infl == 'V':
                    word = lemma[:-2] + 'ieji'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'iųjų'
                elif rqrd_infl == 'N':
                    word = lemma[:-2] + 'iesiems'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'iuosius'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'iaisiais'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'iuosiuose'
            elif rqrd_gen == 'mot':  # neuter or fem
                if rqrd_infl == 'V':
                    word = lemma[:-2] + 'iosios'
                elif rqrd_infl == 'K':
                    word = lemma[:-2] + 'iųjų'
                elif rqrd_infl == 'N':
                    word = lemma[:-2] + 'iosioms'
                elif rqrd_infl == 'G':
                    word = lemma[:-2] + 'iąsias'
                elif rqrd_infl == 'Įn':
                    word = lemma[:-2] + 'iosiomis'
                elif rqrd_infl == 'Vt':
                    word = lemma[:-2] + 'iosiose'

    if word is None:
        return
    else:
        return Numeral(word, real_lemma, num.num_form, num.num_type, rqrd_gen, rqrd_num, rqrd_infl, True, degree=num.degree)


def xpos_to_feats(pos):
    """Transform the XPOS format into the universal FEATS format

    :param pos: the part of speech the XPOS informaton of which needs to be transformed
    :return:
        result      TODO: remove result
        feats       transformed xpos
    """

    #  būtasis dažninis has Iter Aspect in MATAS and Hab aspect in ALKSNIS
    # ALKSNIS has Mood=Nec, which is just dlv in xpos

    all = {'gender':{'mot':'Fem', 'vyr':'Masc', 'bev':'Neut'}, 'number': {'vns': 'Sing', 'dgs': 'Plur'},
           'infl': {'V':'Nom', 'K': 'Gen', 'N': 'Dat', 'G':'Acc', 'Įn':'Ins', 'Vt':'Loc', 'Š':'Voc', 'Il': 'Il'},
           'nums': {'kiek':'Card', 'kelint':'Ord'},
           'tense': {'es':'Pres', 'būt-k':'Past|Aspect=Perf', 'būt-d':'Past|Aspect=Hab', 'būs':'Fut', 'būt':'Past'},
           'mood': {'tiesiog':'Ind', 'tar':'Cnd', 'liep': 'Imp', 'reik':'Nec'}, 'voice': {'neveik':'Pass', 'veik':'Act'},
           'verb_form': {'asm':'Fin', 'dlv':'Part', 'pad':'Ger', 'padlv':'Ger', 'pusd':'Conv', 'bndr':'Inf', 'būdn':'Conv'},
           'polarity':{'neig':'Neg', 'teig':'Pos'}, 'definite':{'įvardž':'Def', 'neįvardž':'Ind'},
           'degree':{'nelygin':'Pos', 'aukšt':'Cmp', 'aukšč':'Sup'}, 'num_form': {'arab':'Digit', 'rom':'Roman', 'mišr':'Combi', 'raid':'Word'},
           'num_type': {'kiek':'Card', 'kelint':'Ord', 'daugin':'Mult', 'kuopin':'Sets', 'trup':'Frac'}}

    result = dict()
    feats = list()

    # find the features and their equivalents in the dictionary of dictionaries
    for a in vars(pos):
        if vars(pos)[a] is not None and a != 'word' and a != 'lemma' \
                and a != 'rflx' and a != 'person' and a != 'proper' and a != 'dfnt':
            result[a] = all[a][vars(pos)[a]]
    if isinstance(pos, Verb):
        if pos.rflx:
            feats.append('Reflex=Yes')
        if pos.person is not None:
            feats.append('Person=' + pos.person)
        for key in result.keys():
            if key == 'gender':
                feats.append('Gender=' + result[key])
            elif key == 'number':
                feats.append('Number=' + result[key])
            elif key == 'infl':
                feats.append('Case=' + result[key])
            elif key == 'tense':
                feats.append('Tense=' + result[key])
            elif key == 'mood':
                feats.append('Mood=' + result[key])
            elif key == 'voice':
                feats.append('Voice=' + result[key])
            elif key == 'verb_form':
                feats.append('VerbForm=' + result[key])
            elif key == 'polarity':
                feats.append('Polarity=' + result[key])
            elif key == 'definite':
                feats.append('Definite=' + result[key])
    else:
        for key in result.keys():
            if key == 'infl':
                feats.append('Case=' + result[key])
            elif key == 'gender':
                feats.append('Gender=' + result[key])
            elif key == 'number':
                feats.append('Number=' + result[key])
            elif key == 'degree':
                feats.append('Degree=' + result[key])
            elif key == 'num_form':
                feats.append('NumForm=' + result[key])
            elif key == 'num_type':
                feats.append('NumType=' + result[key])

        if isinstance(pos, Noun):
            if pos.rflx:
                feats.append('Reflex=Yes')

        if isinstance(pos, Adjective) or isinstance(pos, Numeral):
            if pos.dfnt:
                feats.append('Definite=Def')
            elif (isinstance(pos, Numeral) and pos.num_type) == 'kelint' or isinstance(pos, Adjective):
                feats.append('Definite=Ind')

    # sort alphabetically
    feats = '|'.join(sorted(feats))

    if isinstance(pos, Verb):
        feats_temp = [i.split('=') for i in feats.split('|')]
        feats = ('|').join([i[0] + '=' + i[1] for i in sorted(feats_temp)])

    return result, feats


def verb_to_xpos(verb):
    """Extract xpos from a Verb object

    :param verb: the Verb object
    :return: XPOS information
    """

    xpos = list()
    xpos.append('vksm')

    for a in vars(verb):
        if vars(verb)[a] is not None and a != 'word' and a != 'lemma' \
                and a != 'pres_form' and a != 'past_form':
            if a == 'rflx':
                if vars(verb)[a] == True:
                    xpos.append('sngr')
            elif a == 'definite':
                if vars(verb)[a] == 'įvardž':
                    xpos.append('įvardž')
            elif a == 'polarity':
                if vars(verb)[a] == 'neig':
                    xpos.append('neig')
            else:
                xpos.append(vars(verb)[a])

    xpos = '.'.join(xpos) + '.'

    return xpos


def noun_to_xpos(noun):
    """Extract xpos from a Noun object

    :param noun:    the Noun object
    :return: xpos information
    """

    xpos = list()
    xpos.append('dkt')

    for a in vars(noun):
        if vars(noun)[a] is not None and a != 'word' and a != 'lemma':
            if a == 'proper':
                if vars(noun)[a] == True:
                    xpos.append('tikr')
            elif a == 'rflx':
                if vars(noun)[a] == True:
                    xpos.append('sngr')
            else:
                xpos.append(vars(noun)[a])

    xpos = '.'.join(xpos) + '.'

    return xpos


def adj_to_xpos(adj):
    """Extract xpos from an Adjective object

    :param adj: the Adjective object
    :return: xpos information
    """

    xpos = list()
    xpos.append('bdv')

    xpos.append(vars(adj)['degree'])
    if vars(adj)['dfnt'] == True:
        xpos.append('įvardž')

    for a in vars(adj):
        if vars(adj)[a] is not None and a != 'word' and a != 'lemma' and a != 'degree' and a != 'dfnt':
            xpos.append(vars(adj)[a])

    xpos = '.'.join(xpos) + '.'

    return xpos


def num_to_xpos(num):
    """Extract xpos from a Numeral object

    :param num: the Numeral object
    :return: xpos information
    """

    xpos = list()
    xpos.append('sktv')
    xpos.append(vars(num)['num_form'])
    xpos.append(vars(num)['num_type'])

    if vars(num)['degree'] is not None:
        xpos.append(vars(num)['degree'])
    if vars(num)['dfnt'] == True:
        xpos.append('įvardž')

    for a in vars(num):
        if vars(num)[a] is not None and a != 'word' and a != 'lemma' and a != 'degree' and a != 'dfnt' and a != 'num_type' and a != 'num_form':
            xpos.append(vars(num)[a])

    xpos = '.'.join(xpos) + '.'

    return xpos


def adv_to_xpos(adv):
    """Extract xpos from an Adverb object

    :param num: the Adverb object
    :return: xpos information
    """

    xpos = list()
    xpos.append('prv')

    xpos.append(vars(adv)['degree'])

    xpos = '.'.join(xpos) + '.'

    return xpos

def generate_numerals(fileName):
    """
    Generate numeral paradigms and print them into a .conllu file
    :param fileName: file to write numerals to
    """

    number = ['vns', 'dgs']
    gender = ['mot', 'vyr']
    cases = ['V', 'K', 'N', 'G', 'Įn', 'Vt']

    numerals = list()

    # the main numerals
    two_to_nine = ['du', 'trys', 'keturi', 'penki', 'šeši', 'septyni', 'aštuoni', 'devyni']
    ord_one_to_nine = ['pirmas', 'antras', 'trečias', 'ketvirtas', 'penktas', 'šeštas', 'septintas', 'aštuntas',
                       'devintas']
    eleven_to_nineteen = ['vienuolika', 'dvylika', 'trylika', 'keturiolika', 'penkiolika', 'šešiolika', 'septyniolika',
                          'aštuoniolika', 'devyniolika']
    tens = ['dešimt', 'dvidešimt', 'trisdešimt', 'keturiasdešimt', 'penkiasdešimt', 'šešiasdešimt', 'septyniasdešimt',
            'aštuoniasdešimt', 'devyniasdešimt']
    more = ['šimtas', 'tūkstantis', 'milijonas', 'milijardas']

    kuopin = ['dvejetas', 'trejetas', 'ketvertas', 'penketas', 'šešetas', 'septynetas', 'aštuonetas',
              'devynetas']  # sktv.raid.kuopin.V.

    daugin = ['vieneri', 'dveji', 'treji', 'ketveri', 'penkeri', 'šešeri', 'septyneri', 'aštuoneri', 'devyneri']

    # cardinal plural numbers
    for i in range(len(daugin)):
        n = numeralise(daugin[i], daugin[i], 'sktv.raid.daugin.vyr.V.')
        numerals.append(n)

    # decline the numerals and add them to the main list
    main_numerals = list()
    for u in numerals:
        for g in gender:
            for c in cases:
                main_numerals.append(decline_num(u, c, rqrd_gen=g))

    singles = list()  # declined numerals from 1 to 9

    # unlike other simple cardinal numerals, vienas has number
    v = numeralise('vienas', 'vienas', 'sktv.raid.kiek.vyr.vns.V.')
    for nu in number:
        for g in gender:
            for c in cases:
                main_numerals.append(decline_num(v, c, nu, g))
                if nu == 'vns':
                    singles.append(decline_num(v, c, nu, g))

    for tw in two_to_nine:
        for g in gender:
            for c in cases:
                main_numerals.append(decline_num(numeralise(tw, tw, 'sktv.raid.kiek.vyr.V'), c, rqrd_gen=g))
                singles.append(decline_num(numeralise(tw, tw, 'sktv.raid.kiek.vyr.V'), c, rqrd_gen=g))

    teens = list()
    for e in eleven_to_nineteen:
        for c in cases:
            main_numerals.append(decline_num(numeralise(e, e, 'sktv.raid.kiek.V.'), rqrd_infl=c))
            teens.append(decline_num(numeralise(e, e, 'sktv.raid.kiek.V.'), rqrd_infl=c))

    for t in tens:
        main_numerals.append(numeralise(t, t, 'sktv.raid.kiek.'))
        # decline the feminine version of the tens
        for nu in number:
            for c in cases:
                main_numerals.append(
                    decline_num(numeralise(t + 'is', t + 'is', 'sktv.raid.kiek.mot.vns.V.'), rqrd_infl=c, rqrd_num=nu))
        if t != 'dešimt':
            for k in singles:
                main_numerals.append(numeralise(t + ' ' + k.word, t + ' ' + k.lemma, 'sktv.raid.kiek.' +
                                                (k.gender + '.' if k.gender is not None else '') + '.' +
                                                (k.number + '.' if k.number is not None else '') +
                                                (k.infl + '.' if k.infl is not None else '')))
    # decline cardinal numerals above 99
    for m in more:
        for nu in number:
            for c in cases:
                main_numerals.append(decline_num(numeralise(m, m, 'sktv.raid.kiek.vyr.vns.V.'), c, nu))

    # decline collective numerals
    for k in kuopin:
        for c in cases:
            main_numerals.append(decline_num(numeralise(k, k, 'sktv.raid.kuopin.V.'), rqrd_infl=c))

    # decline ordinal numerals
    singles = list()
    for o in ord_one_to_nine:
        main_numerals.append(numeralise(o[:-1], o, 'sktv.raid.kelint.bev.'))
        singles.append(numeralise(o[:-1], o, 'sktv.raid.kelint.bev.'))
        for nu in number:
            for g in gender:
                for c in cases:
                    main_numerals.append(decline_num(numeralise(o, o, 'sktv.raid.kelint.vyr.vns.V.'), c, nu, g))
                    main_numerals.append(num_def(numeralise(o, o, 'sktv.raid.kelint.vyr.vns.V.'), g, nu, c))
                    singles.append(decline_num(numeralise(o, o, 'sktv.raid.kelint.vyr.vns.V.'), c, nu, g))
                    singles.append(num_def(numeralise(o, o, 'sktv.raid.kelint.vyr.vns.V.'), g, nu, c))

    for e in eleven_to_nineteen:
        for nu in number:
            for g in gender:
                for c in cases:
                    main_numerals.append(
                        decline_num(numeralise(e[:-1] + 'tas', e[:-1] + 'tas', 'sktv.raid.kelint.vyr.vns.V.'), c, nu,
                                    g))
                    main_numerals.append(
                        num_def(numeralise(e[:-1] + 'tas', e[:-1] + 'tas', 'sktv.raid.kelint.vyr.vns.V.'), g, nu, c))

    for t in tens:
        for nu in number:
            for g in gender:
                for c in cases:
                    main_numerals.append(
                        decline_num(numeralise(t + 'as', t + 'as', 'sktv.raid.kelint.vyr.vns.V.'), c, nu, g))
                    main_numerals.append(
                        num_def(numeralise(t + 'as', t + 'as', 'sktv.raid.kelint.vyr.vns.V.'), g, nu, c))
        if t != 'dešimt':
            for k in singles:
                main_numerals.append(numeralise(t + ' ' + k.word, t + ' ' + k.lemma,
                                                'sktv.raid.kelint.' + ('įvardž.' if k.dfnt else '')
                                                + k.gender + '.' + (
                                                    k.number + '.' if k.number is not None else '') + (
                                                    k.infl + '.' if k.infl is not None else '')))

    remaining = list()
    remaining.append(numeralise('šimtas', 'šimtas', 'sktv.raid.kelint.vyr.vns.V.'))
    remaining.append(numeralise('tūkstantas', 'tūkstantas', 'sktv.raid.kelint.vyr.vns.V.'))
    remaining.append(numeralise('milijonas', 'milijonas', 'sktv.raid.kelint.vyr.vns.V.'))
    remaining.append(numeralise('milijardas', 'milijardas', 'sktv.raid.kelint.vyr.vns.V.'))

    remaining.append(numeralise('pirmesnis', 'pirmas', 'sktv.raid.kelint.aukšt.vyr.vns.V.'))
    remaining.append(numeralise('pirmiausias', 'pirmas', 'sktv.raid.kelint.aukšč.vyr.vns.V.'))

    for r in remaining:
        for nu in number:
            for g in gender:
                for c in cases:
                    main_numerals.append(decline_num(r, c, nu, g))
                    main_numerals.append(num_def(r, g, nu, c))

    main_numerals.append(numeralise('pirmiausia', 'pirmas', 'sktv.raid.kelint.aukšč.bev.'))

    w = open(fileName, 'a', encoding='utf8')
    for t in main_numerals:
        xpos = num_to_xpos(t)
        _, feats = xpos_to_feats(t)
        # split multiword tokens into multiple lines
        if len(t.word.split()) == 1:
            w.write('0' + '\t' + t.word + '\t' + t.lemma + '\t' + 'NUM' + '\t' + xpos + '\t' + feats +
                    '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
        elif len(t.word.split()) > 1:
            for i in range(len(t.word.split())):
                if i < len(t.word.split()) - 1:
                    if i == 0:
                        insert = 'sampl.'
                    else:
                        insert = 'tęs.'
                    for m in main_numerals:
                        if m.word == t.word.split()[i] and m.num_type == 'kiek':
                            m_xpos = num_to_xpos(m)
                            _, m_feats = xpos_to_feats(m)
                            w.write(
                                '0' + '\t' + m.word + '\t' + m.lemma + '\t' + 'NUM' + '\t' + insert + m_xpos + '\t' + m_feats +
                                '|Hyph=Yes' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                elif i == len(t.word.split()) - 1:
                    w.write(
                        '0' + '\t' + t.word.split()[i] + '\t' + t.lemma.split()[
                            i] + '\t' + 'NUM' + '\t' + 'tęs.' + xpos + '\t' + feats +
                        '|Hyph=Yes' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')

    w.close()

def generate_freq_numerals(freqFileName, fileName):
    """
    Append the numerals found in the frequent numerals list to the already generated .conllu file
    The list is manually edited to make sure it does not contain any forms that are already in the .conllu file
    :param freqFileName: the list of remaining frequent numerals
    :param fileName: file to append the numerals t
    """

    card_as = ['šimtas', 'milijonas', 'milijardas']

    r = open(freqFileName, 'r', encoding='utf8')
    lines = r.readlines()
    r.close()

    ordinals = list()
    cardinals = list()

    for l in lines:
        word = l.strip()
        # determine the numeral form
        raid = False
        arab = False
        rom = False
        rom_num = ['i', 'x', 'l', 'd', 'c', 'm', 'v']
        for i in range(len(word)):
            if word[i] in rom_num:
                if i < len(word) - 1:
                    if word[i + 1] in rom_num or word[i + 1] == '-' or '-' not in word:
                        rom = True
                    else:
                        raid = True
            elif word[i].isalpha():
                raid = True
            elif word[i].isdigit():
                arab = True

        if (raid and arab) or (raid and rom):
            num_form = 'mišr.'
        elif raid:
            num_form = 'raid.'
        elif rom:
            num_form = 'rom.'
        elif arab:
            num_form = 'arab.'

        if word.endswith('as') and word != 'vienas' and not (word.endswith('etas') or word.endswith('ertas')):
            if word in card_as:
                if word not in ordinals:
                    ordinals.append(numeralise(word, word, 'sktv.' + num_form + 'kelint.vyr.vns.V.'))
                if word not in cardinals:
                    cardinals.append(numeralise(word, word, 'sktv.' + num_form + 'kiek.vyr.vns.V.'))
            else:
                ordinals.append(numeralise(word, word, 'sktv.' + num_form + 'kelint.vyr.vns.V.'))
        elif word.endswith('eji') or word.endswith('eri'):
            cardinals.append(numeralise(word, word, 'sktv.' + num_form + 'daugin.vyr.V.'))

    number = ['vns', 'dgs']
    gender = ['mot', 'vyr']
    cases = ['V', 'K', 'N', 'G', 'Įn', 'Vt']
    w = open(fileName, 'a', encoding='utf8')
    for ca in ordinals:
        for nu in number:
            for g in gender:
                for c in cases:
                    d = decline_num(ca, c, nu, g)
                    xpos = num_to_xpos(d)
                    _, feats = xpos_to_feats(d)
                    w.write('0' + '\t' + d.word + '\t' + d.lemma + '\t' + 'NUM' + '\t' + xpos + '\t' + feats +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                    defin = num_def(ca, g, nu, c)
                    xpos = num_to_xpos(defin)
                    _, feats = xpos_to_feats(defin)
                    w.write('0' + '\t' + defin.word + '\t' + defin.lemma + '\t' + 'NUM' + '\t' + xpos + '\t' + feats +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')

    for o in cardinals:
        for g in gender:
            for c in cases:
                d = decline_num(o, c, rqrd_gen=g)
                xpos = num_to_xpos(d)
                _, feats = xpos_to_feats(d)
                w.write('0' + '\t' + d.word + '\t' + d.lemma + '\t' + 'NUM' + '\t' + xpos + '\t' + feats +
                        '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')

    w.close()
