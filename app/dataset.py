# coding:utf-8
# created by z5089986 

from gensim.models.doc2vec import TaggedDocument
from gensim.utils import simple_preprocess
from db.db_question import DBQue
from db.db_answer import DBAns
from db.db_cquestion import DBCQue
from bs4 import BeautifulSoup
import time
import logging
from gensim.models.callbacks import CallbackAny2Vec
from tools.nltkfilter import nltkfilter


class EpochLogger(CallbackAny2Vec):
    '''This is a class to write the log of specific stages during the training'''
    def __init__(self, logname):
        self.epoch = 0
        self.start_time = time.time()
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        logging.basicConfig(filename="my.log", level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
        logging.info("\n\n\n----------------------------")
        logging.info("{} start".format(logname))

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        print("Epoch #{} end at {}".format(self.epoch, time.time()-self.start_time))
        logging.info("Epoch #{} end".format(self.epoch))

        self.epoch += 1

def decorate(fun):
    '''a function to output the called times of a registered function'''
    count = 0
    begin_time = time.time()

    def wrapper(*args, **kwargs):
        nonlocal count
        start_time = time.time()
        data = fun(*args, **kwargs)
        stop_time = time.time()
        dt = stop_time - begin_time
        count += 1
        if (count % 1000 == 0):
            print("called %d times，%fs cost。" % (count, dt))
        return data

    return wrapper

class TaggedLineDocument():
    '''a class to generate a batch of TaggedDocument Objects,
        this object is the input corpus during training the model'''

    data=[]
    db = ''

    def __init__(self, object):
        self.data = object

    def __iter__(self):
        for uid, line in enumerate(self.data):
            tags = [uid]+line[0]
            yield TaggedDocument(words=line[1], tags=tags)

class Dataset():
    '''this class is a package of some functions for connecting
    the business logic layer and data access layer,
    as well as the some functions for process the input or training data'''

    def __init__(self):
        '''
        create the connection class to the database
        '''
        self.dbQue = DBQue()
        self.dbCque = DBCQue()
        self.dbAns = DBAns()

    @decorate
    def format_question(self, html_text):
        '''
        using the BeautifulSoup function from bs4 library to clean the html tags
        :param html_text: string type, a batch of sentence in html form with some html tags
        :return:string type, a clean sentence, html tags removed
        '''
        soup = BeautifulSoup(html_text, 'lxml')
        question = ' '.join([t.text for t in soup.find_all('p')])
        return question

    def sent_to_word(self, sents):
        '''
        using simple_preprocess function to split sentences into words lists
        :param sents:list type, a batch of sentence
        :return:two-dimension list, with sentences split into words list
        '''
        for sent in sents:
            yield (simple_preprocess(str(sent), deacc=True))

    def sent_nltk_wordself(self, sents):
        '''
        some functions defined in nltkfilter.py to split sentences into
        words lists via using pos_tag tech from NLTK library.
        Verbs and Nouns in the sentence will be remained, other words will be removed.
        :param sents:list type, a batch of sentence
        :return:two-dimension list, with sentences split into words list
        '''
        for sent in sents:
            yield (nltkfilter(str(sent)))


    def query_cquestion(self, count=0):
        '''
        cquestion table query function in the data access layer
        will be called here to perform query
        :param count: the number of rows will be return from then query,
            default value is 0 which means return all query result.
        :return: a list of object of CQuestion class, which is the result of query
        '''
        que = self.dbCque.query_all(count)
        return que

    def get_questions_by_ids(self, ids):
        '''
        Question table query function in the data access layer
        will be called here to perform query via its id
        :param count: a list of id.
        :return: a list of object of Question class, which is the result of query
        '''
        res = []
        for index, i in enumerate(ids):
            if index%1000==0: print(i, index)
            res.append(self.dbQue.query_by_queId(int(i)))
        return res

    def get_question(self, count=0):
        '''
        Question table query function in the data access layer
        will be called here to perform query
        :param count: the number of rows will be return from then query,
            default value is 0 which means return all query result.
        :return: a list of object of Question class, which is the result of query
        '''
        que = self.dbQue.get_questions(count)
        return que

    def get_keywords(self, count=0):
        '''
        Question table query function in the data access layer
        will be called here to perform query, only the value of keywords column will be returned
        :param count: the number of rows will be return from then query,
            default value is 0 which means return all query result.
        :return: a list of object of Question class containing only keywords value, which is the result of query
        '''
        que = self.dbQue.get_keywords_all(self, count)
        return que

    def query_question_by_id(self, id):
        '''
        Question table query function in the data access layer
        will be called here to perform query via its id
        :param count: a single id input.
        :return: a single object of Question class, which is the result of query
        '''
        return self.dbQue.query_by_id(id = int(self, id))

    def get_title_by_queId(self, id):
        '''
        Question table query function in the data access layer
        will be called here to perform query via its question_id, only the value of title column will be returned
        :param count: a single question id input.
        :return: a single object of Question class containing only title value, which is the result of query
        '''
        return self.dbQue.get_title_by_queId(queId=id)

    def get_keywords_by_queId(self, id):
        '''
        Question table query function in the data access layer
        will be called here to perform query via its question_id, only the value of keywords column will be returned
        :param count: a single question id input.
        :return: a single object of Question class containing only keywords value, which is the result of query
        '''
        return self.dbQue.get_keywords_by_queId(queId=id)

    def query_cquestion_by_id(self, id):
        '''
        CQuestion table query function in the data access layer
        will be called here to perform query via its id.
        :param count: a single id input.
        :return: a single object of CQuestion class, which is the result of query
        '''
        return self.dbCque.query_by_id(id = int(id))

    def get_answer_by_queId(self, id):
        '''
        Answer table query function in the data access layer
        will be called here to perform query via its question id.
        :param count: a single question id input.
        :return: a single object of Answer class, which is the result of query
        '''
        return self.dbAns.get_ANS_by_queId(queId = int(id))

