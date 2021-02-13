import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence, pack_sequence, PackedSequence

from stanza.models.common.biaffine import BiaffineScorer
from stanza.models.common.hlstm import HighwayLSTM
from stanza.models.common.dropout import WordDropout
from stanza.models.common.vocab import CompositeVocab
from stanza.models.common.char_model import CharacterModel
from stanza.models.common import utils, data
from stanza.models.pos.hunspeller.huncheck import Hunchecker



class Tagger(nn.Module):
    def __init__(self, args, vocab, doc, emb_matrix=None, share_hid=False, morph_dict=None):  # ADD DOC TO PARAMETERS
        super().__init__()

        self.vocab = vocab
        self.args = args
        self.share_hid = share_hid
        self.unsaved_modules = []

        def add_unsaved_module(name, module):
            self.unsaved_modules += [name]
            setattr(self, name, module)

        # input layers
        input_size = 0
        if self.args['word_emb_dim'] > 0:
            # frequent word embeddings
            self.word_emb = nn.Embedding(len(vocab['word']), self.args['word_emb_dim'], padding_idx=0)
            input_size += self.args['word_emb_dim']

        if not share_hid:
            # upos embeddings
            self.upos_emb = nn.Embedding(len(vocab['upos']), self.args['tag_emb_dim'], padding_idx=0)

        if self.args['char'] and self.args['char_emb_dim'] > 0:
            self.charmodel = CharacterModel(args, vocab)
            self.trans_char = nn.Linear(self.args['char_hidden_dim'], self.args['transformed_dim'], bias=False)
            input_size += self.args['transformed_dim']

        if self.args['pretrain']:
            # pretrained embeddings, by default this won't be saved into model file
            add_unsaved_module('pretrained_emb',
                               nn.Embedding.from_pretrained(torch.from_numpy(emb_matrix), freeze=True))
            self.trans_pretrained = nn.Linear(emb_matrix.shape[1], self.args['transformed_dim'], bias=False)
            input_size += self.args['transformed_dim']

        # recurrent layers
        self.taggerlstm = HighwayLSTM(input_size, self.args['hidden_dim'], self.args['num_layers'], batch_first=True,
                                      bidirectional=True, dropout=self.args['dropout'],
                                      rec_dropout=self.args['rec_dropout'], highway_func=torch.tanh)
        self.drop_replacement = nn.Parameter(torch.randn(input_size) / np.sqrt(input_size))
        self.taggerlstm_h_init = nn.Parameter(torch.zeros(2 * self.args['num_layers'], 1, self.args['hidden_dim']))
        self.taggerlstm_c_init = nn.Parameter(torch.zeros(2 * self.args['num_layers'], 1, self.args['hidden_dim']))

        # classifiers
        self.upos_hid = nn.Linear(self.args['hidden_dim'] * 2, self.args['deep_biaff_hidden_dim'])
        self.upos_clf = nn.Linear(self.args['deep_biaff_hidden_dim'], len(vocab['upos']))
        self.upos_clf.weight.data.zero_()
        self.upos_clf.bias.data.zero_()

        if share_hid:
            clf_constructor = lambda insize, outsize: nn.Linear(insize, outsize)
        else:
            self.xpos_hid = nn.Linear(self.args['hidden_dim'] * 2,
                                      self.args['deep_biaff_hidden_dim'] if not isinstance(vocab['xpos'],
                                                                                           CompositeVocab) else
                                      self.args['composite_deep_biaff_hidden_dim'])
            self.ufeats_hid = nn.Linear(self.args['hidden_dim'] * 2, self.args['composite_deep_biaff_hidden_dim'])
            clf_constructor = lambda insize, outsize: BiaffineScorer(insize, self.args['tag_emb_dim'], outsize)

        if isinstance(vocab['xpos'], CompositeVocab):
            self.xpos_clf = nn.ModuleList()
            for l in vocab['xpos'].lens():
                self.xpos_clf.append(clf_constructor(self.args['composite_deep_biaff_hidden_dim'], l))
        else:
            self.xpos_clf = clf_constructor(self.args['deep_biaff_hidden_dim'], len(vocab['xpos']))
            if share_hid:
                self.xpos_clf.weight.data.zero_()
                self.xpos_clf.bias.data.zero_()

        self.ufeats_clf = nn.ModuleList()
        for l in vocab['feats'].lens():
            if share_hid:
                self.ufeats_clf.append(clf_constructor(self.args['deep_biaff_hidden_dim'], l))
                self.ufeats_clf[-1].weight.data.zero_()
                self.ufeats_clf[-1].bias.data.zero_()
            else:
                self.ufeats_clf.append(clf_constructor(self.args['composite_deep_biaff_hidden_dim'], l))

        # criterion
        self.crit = nn.CrossEntropyLoss(ignore_index=0)  # ignore padding

        self.drop = nn.Dropout(args['dropout'])
        self.worddrop = WordDropout(args['word_dropout'])

        self.doc = doc

    def forward(self, word, word_mask, wordchars, wordchars_mask, upos, xpos, ufeats, pretrained, word_orig_idx,
                sentlens, wordlens, orig_idx=None, morph_dict=None, start=None, end=None):

        def pack(x):  # Packs a Tensor containing padded sequences of variable length.
            return pack_padded_sequence(x, sentlens, batch_first=True)

        inputs = []
        if self.args['word_emb_dim'] > 0:
            word_emb = self.word_emb(word)
            word_emb = pack(word_emb)
            inputs += [word_emb]

        if self.args['pretrain']:
            pretrained_emb = self.pretrained_emb(pretrained)
            pretrained_emb = self.trans_pretrained(pretrained_emb)
            pretrained_emb = pack(pretrained_emb)
            inputs += [pretrained_emb]

        def pad(x):  # inverse operation to pack_padded_sequence(). Pads a packed batch of variable length sequences.
            return pad_packed_sequence(PackedSequence(x, word_emb.batch_sizes), batch_first=True)[0]

        if self.args['char'] and self.args['char_emb_dim'] > 0:
            char_reps = self.charmodel(wordchars, wordchars_mask, word_orig_idx, sentlens, wordlens)
            char_reps = PackedSequence(self.trans_char(self.drop(char_reps.data)), char_reps.batch_sizes)
            inputs += [char_reps]

        lstm_inputs = torch.cat([x.data for x in inputs],1)
        lstm_inputs = self.worddrop(lstm_inputs, self.drop_replacement)
        lstm_inputs = self.drop(lstm_inputs)
        lstm_inputs = PackedSequence(lstm_inputs, inputs[0].batch_sizes)

        lstm_outputs, _ = self.taggerlstm(lstm_inputs, sentlens, hx=(
        self.taggerlstm_h_init.expand(2 * self.args['num_layers'], word.size(0), self.args['hidden_dim']).contiguous(),
        self.taggerlstm_c_init.expand(2 * self.args['num_layers'], word.size(0), self.args['hidden_dim']).contiguous()))
        lstm_outputs = lstm_outputs.data

        upos_hid = F.relu(self.upos_hid(self.drop(lstm_outputs)))
        upos_pred = self.upos_clf(self.drop(upos_hid))
        preds = [pad(upos_pred).max(2)[1]]

        upos = pack(upos).data
        loss = self.crit(upos_pred.view(-1, upos_pred.size(-1)), upos.view(-1))

        if self.share_hid:
            xpos_hid = upos_hid
            ufeats_hid = upos_hid

            clffunc = lambda clf, hid: clf(self.drop(hid))
        else:
            xpos_hid = F.relu(self.xpos_hid(self.drop(lstm_outputs)))
            ufeats_hid = F.relu(self.ufeats_hid(self.drop(lstm_outputs)))

            # this is where we get upos embeddings
            if self.training:
                upos_emb = self.upos_emb(upos)
            else:
                # get the top 5 upos predictions
                best_5 = [sorted(range(len(x)), key=lambda i: x[i], reverse=True)[:5] for x in upos_pred]
                # save upos emb for later
                upos_temp = self.upos_emb
                upos_emb = self.upos_emb(upos_pred.max(1)[1])

            clffunc = lambda clf, hid: clf(self.drop(hid), self.drop(upos_emb))  # ORG

        xpos = pack(xpos).data
        if isinstance(self.vocab['xpos'], CompositeVocab):
            xpos_preds = []
            for i in range(len(self.vocab['xpos'])):
                xpos_pred = clffunc(self.xpos_clf[i], xpos_hid)
                loss += self.crit(xpos_pred.view(-1, xpos_pred.size(-1)), xpos[:, i].view(-1))
                xpos_preds.append(pad(xpos_pred).max(2, keepdim=True)[1])
            preds.append(torch.cat(xpos_preds, 2))
        else:
            xpos_pred = clffunc(self.xpos_clf, xpos_hid)
            loss += self.crit(xpos_pred.view(-1, xpos_pred.size(-1)), xpos.view(-1))
            preds.append(pad(xpos_pred).max(2)[1])

        ufeats_preds = []
        ufeats = pack(ufeats).data
        for i in range(len(self.vocab['feats'])):
            ufeats_pred = clffunc(self.ufeats_clf[i], ufeats_hid)
            loss += self.crit(ufeats_pred.view(-1, ufeats_pred.size(-1)), ufeats[:, i].view(-1))
            ufeats_preds.append(pad(ufeats_pred).max(2, keepdim=True)[1])
        preds.append(torch.cat(ufeats_preds,2))

        # post-filter only if a morphological dictionary is present
        if morph_dict:

            # get the most likely ufeats tag for each top 5 upos tags predicted for a word
            feats_coeffs = list()
            for r in range(5):  # condition ufeats on a different upos tag embedding each time
                upos_2 = torch.LongTensor([x[r] for x in best_5])
                upos_emb2 = upos_temp(upos_2)
                clffunc_temp = lambda clf, hid: clf(self.drop(hid), self.drop(upos_emb2))

                ufeats_preds_temp = []
                for i in range(len(self.vocab['feats'])):
                    ufeats_pred = clffunc_temp(self.ufeats_clf[i], ufeats_hid)
                    ufeats_preds_temp.append(pad(ufeats_pred).max(2, keepdim=True)[1])
                feats_coeffs.append(torch.cat(ufeats_preds_temp, 2))

            # unmap all tags into readable format and unsort them into the original order that matches the sentence order
            upos_seqs = [self.vocab['upos'].unmap(up) for up in preds[0].tolist()]
            xpos_seqs = [self.vocab['xpos'].unmap(up) for up in preds[1].tolist()]
            feats_seqs = [self.vocab['feats'].unmap(up) for up in preds[2].tolist()]
            pred_tokens = [[[upos_seqs[i][j], xpos_seqs[i][j], feats_seqs[i][j]] for j in range(sentlens[i])] for i in
                           range(word.size(0))]
            pred_tokens = utils.unsort(pred_tokens, orig_idx)

            # pair the tags with the right words in the right sentences.
            sntncs = self.doc.sentences[start:end]
            sent_tokens = [[x.text for x in sent.tokens] for sent in sntncs]
            pair = [x for x in zip(sent_tokens, pred_tokens)]

            # 5 most likely upos tags for the token
            coeff = utils.unsort(pad(upos_pred).tolist(), orig_idx)
            coeff_max = [[sorted(range(len(x)), key=lambda i: x[i], reverse=True)[:5] for x in y] for y in coeff]

            # the most likely feats tag for each top 5 predicted upos tag
            fct = []
            for f in feats_coeffs:
                fct.append(utils.unsort(f, orig_idx))
            fct2 = [list(zip(*[fct[0][i], fct[1][i], fct[2][i], fct[3][i], fct[4][i]])) for i in range(len(fct[0]))]
            feats_coeffs = [[list(j[i]) for i in range(len(j))] for j in fct2]

            # initialise hunspell for Lithuanian
            if self.args['lang'] == 'lt':
                hunspell = Hunchecker('lt-LT_morphology', 'D:/Hunspell-Zodynai-ir-gramatika-v.45')

            print('Post-filtering...')
            for p in range(len(pair)):  # get a sentence
                words = pair[p][0]
                tags = pair[p][1]

                a = 0
                while a < len(words):

                    lemma, upos, xpos, feats = morph_dict.find(words[a])
                    if upos is None:
                        lemma, upos, xpos, feats = morph_dict.find(words[a].lower())
                    else:
                        lemma2, upos2, xpos2, feats2 = morph_dict.find(words[a].lower())
                        if lemma2:
                            for i in range(len(lemma2)):
                                if upos2[i] not in upos or feats2[i] not in feats:
                                    lemma += [lemma2[i]]
                                    upos += [upos2[i]]
                                    xpos += [xpos2[i]]
                                    feats += [feats2[i]]

                    if self.args['lang'] == 'lt':
                        if upos is None:
                            lemma, upos, xpos, feats = hunspell.hunspell_to_conll(words[a])
                        else:
                            lemma_h, upos_h, xpos_h, feats_h = hunspell.hunspell_to_conll(words[a])
                            if upos_h is not None:
                                for i in range(len(upos_h)):
                                    if upos_h[i] not in upos or feats_h[i] not in feats:
                                        lemma += [lemma_h[i]]
                                        upos += [upos_h[i]]
                                        xpos += [xpos_h[i]]
                                        feats += [feats_h[i]]

                    if upos is not None:
                        if tags[a][0] not in upos:
                            new_upos = None
                            tag_idx = None
                            if len(upos) > 1:
                                max_values = self.vocab['upos'].unmap(coeff_max[p][a][1:])
                                # go through the values in the order of the most likely one
                                for m in range(len(max_values)):  # for every max upos tag
                                    # found one of the possible predicted values in the upos list
                                    if max_values[m] in upos:
                                        indices = [i for i, x in enumerate(upos) if x == max_values[m]]
                                        if len(indices) > 1:  # more than one upos list items matches the max value item
                                            # check if an exact match can be found, using the most informative ufeats tag
                                            for d in indices:
                                                if feats[d] == self.vocab['feats'].unmap(feats_coeffs[p][a][1:])[m] and \
                                                        upos[d] == max_values[m]:
                                                    new_upos = upos[d]
                                                    tag_idx = d
                                                    break
                                        if len(indices) == 1 or new_upos is None:
                                            new_upos = max_values[m]
                                            tag_idx = upos.index(max_values[m])
                                        break
                                if new_upos is None:  # last resort
                                    new_upos = upos[0]
                                    tag_idx = 0
                            else:  # only one item in upos list
                                new_upos = upos[0]
                                tag_idx = 0

                            new_xpos = xpos[tag_idx]
                            new_feats = feats[tag_idx]
                            # let the tagger deal with multiword tokens itself
                            if ('Hyph=Yes' not in new_feats and 'Hyph=Yes' in tags[a][2]) or (
                                    'Hyph=Yes' in new_feats and 'Hyph=Yes' not in tags[a][2]):
                                new_upos = new_xpos = new_feats = None

                            if new_upos is not None:
                                preds[0][orig_idx.index(p)][a] = self.vocab['upos'].map([new_upos])[0]
                                # sme has a 2D torch here, LT has 3D
                                if not isinstance(self.vocab['xpos'], CompositeVocab):
                                    preds[1][orig_idx.index(p)][a] = self.vocab['xpos'].map([new_xpos])[0]
                                else:
                                    preds[1][orig_idx.index(p)][a] = torch.LongTensor(
                                        self.vocab['xpos'].map([new_xpos])[0])
                                preds[2][orig_idx.index(p)][a] = torch.LongTensor(
                                    self.vocab['feats'].map([new_feats])[0])

                        else:
                            new_xpos = new_feats = None
                            all_found = False
                            for x in range(len(xpos)):
                                if tags[a][1] == xpos[x] and tags[a][2] == feats[x] and upos[x] == tags[a][0]:
                                    all_found = True
                                    break

                            if not all_found:
                                if len(upos) == 1 or (False not in [feats[a] == feats[a + 1] for a in
                                                                    range(len(feats) - 1)] and False not in [
                                                          upos[a] == upos[a + 1] for a in range(len(upos) - 1)]):
                                    new_feats = feats[0]
                                    if '*' not in tags[a][1]:
                                        new_xpos = xpos[0]
                                    all_found = True

                            if not all_found:
                                if len([i for i, x in enumerate(upos) if x == tags[a][0]]) == 1:
                                    new_feats = feats[upos.index(tags[a][0])]
                                    if '*' not in tags[a][1]:
                                        new_xpos = xpos[upos.index(tags[a][0])]
                                    all_found = True

                            if not all_found:
                                found_ft = False
                                for x in range(len(xpos)):
                                    if tags[a][2] == feats[x] and upos[x] == tags[a][0]:
                                        found_ft = True
                                        if xpos[x] != tags[a][1] and '*' not in tags[a][1]:
                                            new_xpos = xpos[x]
                                        break

                                if not found_ft:
                                    for x in range(len(xpos)):
                                        if tags[a][1] == xpos[x] and tags[a][2] != feats[x] and upos[x] == tags[a][0]:
                                            new_feats = feats[x]
                                            break

                            if new_feats:
                                if ('Hyph=Yes' not in new_feats and 'Hyph=Yes' in tags[a][2]) or (
                                        'Hyph=Yes' in new_feats and 'Hyph=Yes' not in tags[a][2]):
                                    # let the tagger deal with multiword tokens itself
                                    new_xpos = new_feats = None

                            if new_xpos is not None:
                                # non composite has a 2D torch here, composite has 3D
                                if not isinstance(self.vocab['xpos'], CompositeVocab):
                                    preds[1][orig_idx.index(p)][a] = self.vocab['xpos'].map([new_xpos])[0]
                                else:
                                    preds[1][orig_idx.index(p)][a] = torch.LongTensor(
                                        self.vocab['xpos'].map([new_xpos])[0])
                            if new_feats is not None:
                                preds[2][orig_idx.index(p)][a] = torch.LongTensor(
                                    self.vocab['feats'].map([new_feats])[0])

                    a += 1

        print('Post-filtering complete.')
        return loss, preds
