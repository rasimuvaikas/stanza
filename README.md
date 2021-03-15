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

A morphological dictionary in CONLL-U format, stored as a MySQL table, is necessary for the filter to be activated, and is accessed through stanza/stanza/models/pos/morph.py.

To obtain filtered predictions run `python -m stanza.models.tagger` in the command line along with the following args:

- --wordvec_dir (path to the pretrained embeddings directory)
- --eval_file (path to a tokenized file to make predictions on)
- --output_file (path to the predicted output file)
- --lang (language code, e.g.: lt for Lithuanian, sme for North Sami)
- --shorthand (language shorthand made up of language code, underscore, and treebank name, e.g.: lt_alksnis, sme_giella)
- --mode predict
- --save_dir (path to the directory where the pretrained model is stored)
- --save_name (name of the pretrained model)
- --morph_dict (name of the MySQL table storing the morphological dictionary)


## LICENSE

Stanza is released under the Apache License, Version 2.0. See the [LICENSE](https://github.com/stanfordnlp/stanza/blob/master/LICENSE) file for more details.
