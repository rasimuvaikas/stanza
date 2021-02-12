from stanza.models.common.doc import Document
from stanza.utils.conll import CoNLL
from collections import Counter
import gzip
import shutil
from stanza.models.pos.vocab import CharVocab, WordVocab, XPOSVocab, FeatureVocab, MultiVocab
import mysql.connector
import configparser

'''Connect to a morphological dictionary and retrieve a word and its information'''

class MorphDictionary():

    def __init__(self, table_name):

        config = configparser.ConfigParser()
        config.read('config.properties')

        self.mydb = mysql.connector.connect(
        host=config["myDB"]["host"],
        user=config["myDB"]["user"],
        password=config["myDB"]["password"],
        database=config["myDB"]["database"])
        self.mydb.set_charset_collation('utf8mb4', 'utf8mb4_unicode_520_ci')
        
        self.db = table_name
        self.myc = self.mydb.cursor()

    def find(self, word):

        lemmas = list()
        upos = list()
        xpos = list()
        feats = list()
        
        self.myc.execute("select word, lemma, upos, xpos, feats from " + self.db + " where word = '" + word + "'")
        myresult = self.myc.fetchall()
        
        if len(myresult) < 1:
            return None, None, None, None
        else:
            for m in myresult:
                if m[0] == word:  # make sure the words are actually the same and not mixed up due to utf8 issues
                    lemmas += [m[1]]
                    upos += [m[2]]
                    xpos += [m[3]]
                    feats += [m[4]]
            if len(lemmas) > 0:
                return lemmas, upos, xpos, feats
            else:
                return None, None, None, None