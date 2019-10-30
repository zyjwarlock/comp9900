# created by z5089986 

from sqlalchemy import Column,Integer,Text,DateTime
from gensim.utils import simple_preprocess
from bs4 import BeautifulSoup
import time
from six import iteritems
from gensim import corpora
from tools.nltkfilter import nltkfilter, gettoken
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collection.sqlite' #setting the database path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
base = SQLAlchemy(app)

class Label(base.Model):
    '''
    class of Label table in database
    '''
    __tablename__ = 'Label'
    id = Column(Integer, primary_key=True)
    label = Column(Text, nullable=False)
    update_time = Column(DateTime, nullable=False)

class Tag(base.Model):
    '''
    class of Tag table in database
    '''
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, nullable=False)
    label_id = Column(Integer, nullable=False)
    update_time = Column(DateTime, nullable=False)

class Question(base.Model):
    '''
    class of Question table in database
    '''
    __tablename__ = 'Question'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, unique=True, nullable=False)
    title = Column(Text, nullable=False)
    questions = Column(Text, nullable=True)
    update_time = Column(DateTime, nullable=False)
    keywords = Column(Text, nullable=True)
    nltkwords = Column(Text, nullable=True)

class Ansewr(base.Model):
    '''
    class of Answer table in database
    '''
    __tablename__ = 'Answer'
    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, unique=True, nullable=False)
    question_id  = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    answers = Column(Text, nullable=True)
    update_time = Column(DateTime, nullable=True)

class CQuestion(base.Model):
    '''
    class of CQuestion table in database
    '''
    __tablename__ = 'CQuestion'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, unique=True, nullable=False)
    label = Column(Text, nullable=False)


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
        if(count%1000==0):
            print("called %d times，%fs cost。" % (count, dt))
        return data
    return wrapper

@decorate
def format_question(html_text):
    '''
    using the BeautifulSoup function from bs4 library to clean the html tags
    :param html_text: string type, a batch of sentence in html form with some html tags
    :return:string type, a clean sentence, html tags removed
    '''
    soup = BeautifulSoup(html_text, 'lxml')
    question = ' '.join([t.text for t in soup.find_all('p')])
    return question

def sent_to_word(sents):
    '''
    using simple_preprocess function to split sentences into words lists
    :param sents:list type, a batch of sentence
    :return:two-dimension list, with sentences split into words list
    '''
    for sent in sents:
        yield (simple_preprocess(str(sent), deacc=True))

def sent_nltk_word(sents):
    '''
    some functions defined in nltkfilter.py to split sentences into
    words lists via using pos_tag tech from NLTK library.
    Verbs and Nouns in the sentence will be remained, other words will be removed.
    :param sents:list type, a batch of sentence
    :return:two-dimension list, with sentences split into words list
    '''
    for sent in sents:
        yield (nltkfilter(str(sent)))

def build_dictionary(corppath='', lines=[], dicsavepath='', cleanedpath='', freq=1):
    '''

    :param corppath:string type, file path, if it does not equal to '',
            a batch of sentence will be loaded from this file as data source
    :param lines: list type, a list of sentence, if corppath is '', this param will be the data source
    :param dicsavepath: string type, dict saving path, if dicsavepath no null, a dictionary,
            with word as key and frequency as value, will be saved.
    :param cleanedpath: string type, file saving path, if cleanedpath no null, sentences after cleaning will saved.
    :param freq: int, the word with frequency less than freq will be removed.
    :return: list, cleand list of key words of each sentence will be returned
    '''
    if lines:
        data_lines = lines
    else:
        with open(corppath, 'r', encoding='utf-8') as file:
            data_lines = file.readlines()

    data_lines = [gettoken(line) for line in data_lines if line!='']
    # data_lines = [stopword(line) for line in data_lines]


    dict = corpora.Dictionary(line for line in data_lines)
    print(dict)
    once_ids = [tokenid for tokenid, docfreq in iteritems(dict.dfs) if docfreq <= freq]

    data_lines = [[word for word in line if dict.token2id[word] not in once_ids] for line in data_lines]


    print('once id len', len(once_ids))
    dict.filter_tokens(once_ids)
    dict.compactify()
    if dicsavepath:
        dict.save(dicsavepath)

    print(dict)

    if cleanedpath:
        with open(cleanedpath, 'w') as file:
            w_file = [file.write(' '.join(line)+'\n') for line in data_lines]
    else:
        print(data_lines)
        return data_lines
