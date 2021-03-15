import configparser
import os
import time
import shutil
import gzip

import mysql.connector

from prep.scrape_sami import get_pos, sme_to_conllu
"""
Create MySQL tables storing North Sami morphological dictionaries
"""


def collect_conllu(freqFile):
    """
    Find the inflectional paradigms of the most frequent North Sami lemmas, and store them in .conllu files
    :param freqFile: the most frequent lemma list, in this case the list available at
    http://hdl.handle.net/11509/106, provided by Giellatekno - Saami Language
    Technology, UiT The Arctic University of Norway; The Divvun group at UiT The Arctic University of Norway and
    The Divvun group at UiT The Arctic University of Norway, 2015, North Saami lemma frequency list,
    Common Language Resources and Technology Infrastructure Norway (CLARINO) Bergen Repository
    """
    o = open(freqFile, 'r', encoding='utf8')
    lines = o.readlines()
    o.close()

    w = open('pos_files/sme_adpositions.conllu', 'w', encoding='utf-8')
    for line in lines:
        l = line.split()
        if len(l) < 3:
            continue
        if l[2] == 'Po':
            w.write('0' + '\t' + l[1] + '\t' + l[1] + '\t' + 'ADP' + '\t'
                + 'Po' + '\t' + '_' + '\t' + '_' +
                '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
        if l[2] == 'Pr':
            w.write('0' + '\t' + l[1] + '\t' + l[1] + '\t' + 'ADP' + '\t'
                + 'Pr' + '\t' + '_' + '\t' + '_' +
                '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
    w.close()

    w = open('pos_files/sme_interjections.conllu', 'w', encoding='utf-8')
    for line in lines:
        l = line.split()
        if len(l) < 3:
            continue
        if l[2] == 'Interj':
            w.write('0' + '\t' + l[1] + '\t' + l[1] + '\t' + 'INTJ' + '\t'
                + 'Interj' + '\t' + '_' + '\t' + '_' +
                '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
    w.close()

    w = open('pos_files/sme_conjunctions.conllu', 'w', encoding='utf-8')
    for line in lines:
        l = line.split()
        if len(l) < 3:
            continue
        if l[2] == 'CC':
            w.write('0' + '\t' + l[1] + '\t' + l[1] + '\t' + 'CCONJ' + '\t'
                + 'CC' + '\t' + '_' + '\t' + '_' +
                '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
        if l[2] == 'CS':
            w.write('0' + '\t' + l[1] + '\t' + l[1] + '\t' + 'SCONJ' + '\t'
                + 'CS' + '\t' + '_' + '\t' + '_' +
                '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
    w.close()

    w = open('pos_files/sme_particles.conllu', 'w', encoding='utf-8')
    for line in lines:
        l = line.split()
        if len(l) < 3:
            continue
        if l[2] == 'Pcle':
            w.write('0' + '\t' + l[1] + '\t' + l[1] + '\t' + 'PART' + '\t'
                + 'Pcle' + '\t' + '_' + '\t' + '_' +
                '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
    w.close()

    for line in lines:
        l = line.split()
        if len(l) < 3:
            continue
        if l[1].startswith('http') or l[1].startswith('www') or '.' in l[1]:
            continue
        if l[2] == 'Num':
            if l[1].isdigit():
                w = open('pos_files/sme_numerals.conllu', 'a', encoding='utf-8')
                w.write(l[1] + '\t' + l[1] + '\t' + 'Num Sg Nom' + '\n')
                endings = [':n', ':i', ':s', ':in', ':t', ':id', ':id', ':ide', ':in', ':iguin']
                cases = ['Num Ess', 'Num Sg Ill', 'Num Sg Loc', 'Num Sg Com', 'Num Pl Nom', 'Num Pl Gen', 'Num Pl Acc',
                         'Num Pl Ill', 'Num Pl Loc', 'Num Pl Com']
                for e in range(len(endings)):
                    w.write('0' + '\t' + l[1] + endings[e] + '\t' + l[1] + '\t' + 'NUM' + '\t'
                            + sme_to_conllu('Num', l[1] + endings[e] + '\t' + l[1] + '\t' + cases[e])[1] + '\t'
                            + sme_to_conllu('Num', l[1] + endings[e] + '\t' + l[1] + '\t' + cases[e])[0] + '\t' + '_' +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                w.close()
            else:
                time.sleep(1)
                forms, feats = get_pos('Num', l[1])
                if forms and feats:
                    w = open('pos_files/sme_numerals.conllu', 'a', encoding='utf-8')
                    for i in range(len(feats)):
                        w.write('0' + '\t' + l[0] + '\t' + l[1] + '\t' + 'NUM' + '\t'
                                + sme_to_conllu('Num', forms[i] + '\t' + l[1] + '\t' + feats[i])[1] + '\t' +
                                sme_to_conllu('Num', forms[i] + '\t' + l[1] + '\t' + feats[i])[0] + '\t' + '_' +
                                '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                    w.close()

        elif l[2] == 'N':
            time.sleep(1)
            forms, feats = get_pos('N', l[1])
            upos = 'NOUN'
            if forms and feats:
                w = open('pos_files/sme_nouns.conllu', 'a', encoding='utf-8')
                for i in range(len(feats)):
                    if 'Prop' in feats[i]:
                        upos = 'PROPN'
                    w.write('0' + '\t' + l[0] + '\t' + l[1] + '\t' + upos + '\t'
                            + sme_to_conllu('N', forms[i] + '\t' + l[1] + '\t' + feats[i])[1] + '\t' +
                            sme_to_conllu('N', forms[i] + '\t' + l[1] + '\t' + feats[i])[0] + '\t' + '_' +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                w.close()
        elif l[2] == 'A':
            time.sleep(1)
            forms, feats = get_pos('A', l[1])
            if forms and feats:
                w = open('pos_files/sme_adjectives.conllu', 'a', encoding='utf-8')
                for i in range(len(feats)):
                    w.write('0' + '\t' + l[0] + '\t' + l[1] + '\t' + 'ADJ' + '\t'
                            + sme_to_conllu('A', forms[i] + '\t' + l[1] + '\t' + feats[i])[1] + '\t' +
                            sme_to_conllu('A', forms[i] + '\t' + l[1] + '\t' + feats[i])[0] + '\t' + '_' +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                w.close()
        elif l[2] == 'Adv':
            time.sleep(1)
            forms, feats = get_pos('Adv', l[1])
            if forms and feats:
                w = open('pos_files/sme_adverbs.conllu', 'a', encoding='utf-8')
                for i in range(len(feats)):
                    w.write('0' + '\t' + l[0] + '\t' + l[1] + '\t' + 'ADV' + '\t'
                            + sme_to_conllu('Adv', forms[i] + '\t' + l[1] + '\t' + feats[i])[1] + '\t' +
                            sme_to_conllu('Adv', forms[i] + '\t' + l[1] + '\t' + feats[i])[0] + '\t' + '_' +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                w.close()
        elif l[2] == 'Pron':
            time.sleep(1)
            forms, feats = get_pos('Pron', l[1])
            if forms and feats:
                w = open('pos_files/sme_pronouns.conllu', 'a', encoding='utf-8')
                for i in range(len(feats)):
                    w.write('0' + '\t' + l[0] + '\t' + l[1] + '\t' + 'PRON' + '\t'
                            + sme_to_conllu('Pron', forms[i] + '\t' + l[1] + '\t' + feats[i])[1] + '\t' +
                            sme_to_conllu('Pron', forms[i] + '\t' + l[1] + '\t' + feats[i])[0] + '\t' + '_' +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                w.close()
        elif l[2] == 'V':
            time.sleep(1)
            forms, feats = get_pos('V', l[1])
            if forms and feats:
                w = open('pos_files/sme_verbs.conllu', 'a', encoding='utf-8')
                for i in range(len(feats)):
                    w.write('0' + '\t' + l[0] + '\t' + l[1] + '\t' + 'VERB' + '\t'
                            + sme_to_conllu('V', forms[i] + '\t' + l[1] + '\t' + feats[i])[1] + '\t' +
                            sme_to_conllu('V', forms[i] + '\t' + l[1] + '\t' + feats[i])[0] + '\t' + '_' +
                            '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
                w.close()


if __name__ == '__main__':

    # read mysql login data
    parent = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
    config = configparser.ConfigParser()
    config.read(os.path.join(parent, 'stanza/models/pos/config.properties'))

    mydb = mysql.connector.connect(
        host=config["myDB"]["host"],
        user=config["myDB"]["user"],
        password=config["myDB"]["password"])
    mydb.set_charset_collation('utf8mb4', 'utf8mb4_unicode_520_ci')

    myc = mydb.cursor()

    # create database if necessary
    myc.execute('CREATE DATABASE IF NOT EXISTS morph')

    mydb = mysql.connector.connect(
        host=config["myDB"]["host"],
        user=config["myDB"]["user"],
        password=config["myDB"]["password"],
        database=config["myDB"]["database"],
        allow_local_infile=True)
    mydb.set_charset_collation('utf8mb4', 'utf8mb4_unicode_520_ci')

    myc = mydb.cursor()

    # create table
    myc.execute('CREATE TABLE sme (id int, word NVARCHAR(500), lemma NVARCHAR(500), '
                'upos NVARCHAR(500), xpos NVARCHAR(500), feats NVARCHAR(500), head NVARCHAR(500),'
                'deprel NVARCHAR(500), deps NVARCHAR(500), misc NVARCHAR(500))')

    # load conllu files into the table
    ROOT = os.getcwd()
    for f in os.listdir(ROOT + '/pos_files'):
        if os.path.isfile(os.path.join(ROOT + '/pos_files', f)):
            myc.execute("LOAD DATA LOCAL INFILE '%s' INTO TABLE sme" %('pos_files/' + f))
            mydb.commit()
            print(f, 'done')
        else:
            if f == 'nouns':
                for o in os.listdir(os.path.join(ROOT + '/pos_files', f)):
                    with gzip.open(os.path.join(ROOT + '/pos_files', f) + '/' + o, 'rb') as f_in:
                        with open('nouns.conllu', 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    myc.execute("LOAD DATA LOCAL INFILE '%s' INTO TABLE sme" %('nouns.conllu'))
                    mydb.commit()
                    print(f, o, 'done')
            else:
                for o in os.listdir(os.path.join(ROOT + '/pos_files', f)):
                    myc.execute("LOAD DATA LOCAL INFILE '%s' INTO TABLE sme" %('pos_files/' + f + '/' + o))
                    mydb.commit()
                    print(f, o, 'done')

    # add giella training data:
    w = open('giella.conllu', 'w', encoding='utf-8')
    r = open('sme_giella-ud-train.conllu', 'r', encoding='utf8')
    lines = r.readlines()
    r.close()
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        w.write(line)
    w.close()

    myc.execute("LOAD DATA LOCAL INFILE '%s' INTO TABLE sme" %('giella.conllu'))
    mydb.commit()

    # add index for faster look-up
    myc.execute("ALTER TABLE sme ADD INDEX(word)")
    mydb.commit()
