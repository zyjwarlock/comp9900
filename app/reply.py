# created by z5089986 
from app.gensim_similarity import similarity_keyword
import time
from tools.nltkfilter import nltkfilter, gettoken

def reply(question):
    '''
    reply 3 most matched QA pairs to the UI
    :param question: string type, input question
    :return:dictionary type, with question as the key and answer as the value
    '''
    start_time = time.time()

    # using the gettoken function defined in nltkfilter.py to extract the key words and store in a list
    question = gettoken(question)

    if(not question): return {}

    # call the similarity_keyword function to compute get the top 3 most matched QA pairs.
    res = similarity_keyword(question)

    print("time cost: ", time.time()-start_time)
    return res
