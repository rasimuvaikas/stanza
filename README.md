<div align="center"><img src="https://github.com/stanfordnlp/stanza/raw/dev/images/stanza-logo.png" height="100px"/></div>

<h2 align="center">Stanza: A Python NLP Library for Many Human Languages</h2>

<div align="center">
    <a href="https://travis-ci.com/stanfordnlp/stanza">
        <img alt="Travis Status" src="https://travis-ci.com/stanfordnlp/stanza.svg?token=RPNzRzNDQRoq2x3J2juj&branch=master">
    </a>
    <a href="https://pypi.org/project/stanza/">
        <img alt="PyPI Version" src="https://img.shields.io/pypi/v/stanza?color=blue">
    </a>
    <a href="https://anaconda.org/stanfordnlp/stanza">
        <img alt="Conda Versions" src="https://img.shields.io/conda/vn/stanfordnlp/stanza?color=blue&label=conda">
    </a>
    <a href="https://pypi.org/project/stanza/">
        <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/stanza?colorB=blue">
    </a>
</div>

## A Fork Implementing a Morphologically Informed Prediction Filtering Mechanism in the POS Tagger

The post-filtering mechanism has been developed for Lithuanian and North Sami models, but can also be used with other pretrained taggers in prediction mode.

A morphological dictionary in CONLL-U format, stored as a MySQL table, is necessary for the filter to be activated, and is accessed through `stanza/stanza/models/pos/morph.py`.  
Edit `stanza/stanza/models/pos/config.properties` and run `stanza/data_files/sme/morph_dict/table_filler.py` and `stanza/data_files/lt/morph_dict/table_filler.py` to create the MySQL tables.


To obtain filtered predictions run `python -m stanza.models.tagger` in the command line along with the following args:

- --wordvec_dir (path to the pretrained embeddings directory)
- --eval_file (path to a tokenized file to make predictions on)
- --output_file (path to the predicted output file)
- --lang (language code, e.g.: lt for Lithuanian, sme for North Sami)
- --shorthand (language shorthand made up of language code, underscore, and treebank name, e.g.: lt_alksnis, sme_giella)
- --mode predict
- --save_dir (path to the directory where the pretrained model is stored)
- --save_name (name of the pretrained model)
- --morph_dict (name of the MySQL table storing the morphological dictionary (e.g.: lt for Lithuanian, sme for North Sami)

For pretrained models refer to https://stanfordnlp.github.io/stanza/download_models.html

## Downloading pretrained embeddings without using the .sh script

* Lithuanian:  
  Download from https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.lt.vec  
  Rename the .vec file to `lt.vectors`, compress it into .xz and place it in a directory with the following path : `embedding_directory_name/fasttext/Lithuanian`

* North Sami:
  Download from https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.se.zip  
  Rename the .vec file to `sme.vectors`, compress it into .xz and place it in a directory with the following path : `embedding_directory_name/fasttext/North_Sami`


##

The repository contains data files collected from the following sources:

* https://github.com/Semantika2/Hunspell-Zodynai-ir-gramatika-v.45:  
  `stanza/data_files/hunspell/lt-LT_morphology.aff`  
  `stanza/data_files/hunspell/lt-LT_morphology.dic`  

* https://github.com/UniversalDependencies/UD_Lithuanian-ALKSNIS/tree/master:  
  `stanza/data_files/lt/lt_alksnis-ud-test.conllu`  
  `stanza/data_files/lt/morph_dict/lt_alksnis-ud-train.conllu`  
  `stanza/data_files/lt/morph_dict/lt_alksnis-ud-dev.conllu`  
 
* https://github.com/UniversalDependencies/UD_North_Sami-Giella/tree/master:  
  `stanza/data_files/sme/sme_giella-ud-test.conllu`  
  `stanza/data_files/sme/morph_dict/sme_giella-ud-train.conllu`

* https://hdl.handle.net/20.500.12259/45817:  
  `stanza/frequent_lemma_study/lt/freqs_found.txt`  
  
* http://hdl.handle.net/11509/106:  
  `stanza/frequent_lemma_study/sme/freqs_found.txt`  









## LICENSE

Stanza is released under the Apache License, Version 2.0. See the [LICENSE](https://github.com/stanfordnlp/stanza/blob/master/LICENSE) file for more details.
