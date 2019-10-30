# coding:utf-8
# created by z5089986 

import os
from gensim.models import doc2vec
from app.dataset import TaggedLineDocument
import numpy as np
import time
from app.dataset import EpochLogger

def gen_d2v_corpus(lines, savemodel, savekv, epcho, istran=False):
    '''
    train the model
    :param lines: list type, a batch of key word list
    :param savemodel: path of saving model
    :param savekv: path of saving key-vector model
    :param epcho: iteration times of training
    :param istran: any existing model already be trained
    :return: None
    '''
    total_examples = len(lines)

    sents = TaggedLineDocument(lines)

    if os.path.exists(savemodel):# ny existing model already be trained
        print('loading model', savemodel, time.asctime())
        model = doc2vec.Doc2Vec.load(savemodel)
        print('loaded model', savemodel, time.asctime())
        if istran:
            count = 0
            while (True):
                count += 1
                epoches = 20
                model.train(sents, total_examples=total_examples, epochs=epoches)
                if count % 10:
                    model.save(savemodel + "." + str(count))
                    model.save(savemodel)
                print('trained ', count * epoches)
    else:
        print('train new model')

        #set the attributes of the model
        model = doc2vec.Doc2Vec(dm_concat=1, dm_tag_count=2, vector_size=300, window=12,
                                min_count=1, workers=4, dm=0)
        model.build_vocab(sents)
        logname = "tag" + str(epcho)
        epoch_logger = EpochLogger(logname)#object of log class
        print('train', time.asctime())
        #train the model
        model.train(sents, total_examples=total_examples, epochs=epcho, callbacks=[epoch_logger])

        #save model
        model.save(savemodel)
        model.wv.save(savekv)


def sent2vec(model, words):
    '''
    have not been used in current project
    :param model:
    :param words:
    :return:
    '''
    vect_list = []
    for w in words:
        try:
            vect_list.append(model.wv[w])
        except:
            continue
    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    return vect / np.sqrt((vect ** 2).sum())

def run(questions, filename='', epcho=20):
    #set path and run the training model
    savemodel = 'tagModel/'+ filename+str(epcho) +'.model'
    savekv = 'tagModel/' + filename+str(epcho) + '_kv.model'
    gen_d2v_corpus(questions, savemodel, savekv, epcho, istran=False)
