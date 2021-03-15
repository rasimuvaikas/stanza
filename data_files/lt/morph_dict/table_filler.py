from stanza.models.pos.hunspeller.decline import generate_numerals, generate_freq_numerals
import os
import mysql.connector
import configparser

"""
Create MySQL tables storing Lithuanian morphological dictionaries
"""

if __name__ == '__main__':

    # generate and add numerals to the manually produced list
    # generate_numerals('pos_files/numerals.conllu')
    # generate_freq_numerals('pos_files/freq_numerals.txt', 'pos_files/numerals.conllu')

    # create and fill mysql table
    parent = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
    config = configparser.ConfigParser()
    config.read(os.path.join(parent, 'stanza/models/pos/config.properties'))

    mydb = mysql.connector.connect(
        host=config["myDB"]["host"],
        user=config["myDB"]["user"],
        password=config["myDB"]["password"])
    mydb.set_charset_collation('utf8mb4', 'utf8mb4_unicode_520_ci')

    myc = mydb.cursor()
    myc.execute('CREATE DATABASE IF NOT EXISTS morph')

    mydb = mysql.connector.connect(
        host=config["myDB"]["host"],
        user=config["myDB"]["user"],
        password=config["myDB"]["password"],
        database=config["myDB"]["database"],
        allow_local_infile=True)
    mydb.set_charset_collation('utf8mb4', 'utf8mb4_unicode_520_ci')

    myc = mydb.cursor()
    myc.execute('CREATE TABLE lt (id int, word NVARCHAR(500), lemma NVARCHAR(500), '
                'upos NVARCHAR(500), xpos NVARCHAR(500), feats NVARCHAR(500), head NVARCHAR(500),'
                'deprel NVARCHAR(500), deps NVARCHAR(500), misc NVARCHAR(500))')

    # load conllu files into the table
    ROOT = os.getcwd()
    for f in os.listdir(ROOT + '/pos_files'):
        myc.execute("LOAD DATA LOCAL INFILE '%s' INTO TABLE lt" %('pos_files/' + f))
        mydb.commit()

    # add alksnis training data:
    w = open('alksnis.conllu', 'w', encoding='utf-8')
    files = ['lt_alksnis-ud-train.conllu', 'lt_alksnis-ud-dev.conllu']
    for f in files:
        r = open(f, 'r', encoding='utf8')
        lines = r.readlines()
        r.close()
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
            w.write(line)
    w.close()
    myc.execute("LOAD DATA LOCAL INFILE '%s' INTO TABLE lt" %('alksnis.conllu'))
    mydb.commit()

    # add index for faster look-up
    myc.execute("ALTER TABLE lt ADD INDEX(word)")
    mydb.commit()






