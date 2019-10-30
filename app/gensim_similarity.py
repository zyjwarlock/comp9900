# created by z5089986 
from gensim.models import doc2vec
from app.dataset import Dataset
import time


print('loading', time.asctime())
'''
load the 3 models, having different training epochs, when the program begin.
'''
kw1_model = doc2vec.Doc2Vec.load("tagModel/keyword20.model", mmap='r')
kw2_model = doc2vec.Doc2Vec.load("tagModel/keyword25.model", mmap='r')
kw3_model = doc2vec.Doc2Vec.load("tagModel/keyword30.model", mmap='r')
dt = Dataset()
print('loaded', time.asctime())


def similarity_keyword(question):
    '''
    To compute the similarity, and return the top 3 most similar matched question and its answer.
    :param question: a list of key words
    :return: a dictionary with 3 key-value pairs, with question as the key and the answer as value.
    '''

    sim = [None for i in range(9)]

    '''transform the key words into vectors, using various training epochs in different model'''
    print('train', time.asctime())
    sim[0] = kw1_model.infer_vector(question, epochs=15)
    sim[1] = kw1_model.infer_vector(question, epochs=20)
    sim[2] = kw1_model.infer_vector(question, epochs=25)
    sim[3] = kw2_model.infer_vector(question, epochs=20)
    sim[4] = kw2_model.infer_vector(question, epochs=25)
    sim[5] = kw2_model.infer_vector(question, epochs=30)
    sim[6] = kw3_model.infer_vector(question, epochs=25)
    sim[7] = kw3_model.infer_vector(question, epochs=30)
    sim[8] = kw3_model.infer_vector(question, epochs=35)
    print('train', time.asctime())

    '''using the vectors we got above to compute the similarity, 
        top 10 most similar matched question, including index and similarity, 
        in data source will be returned.
        Totally, 9 times of matching have been processed, each time return a list which contains 10 pairs of 
        index and similarity order by descending similarity. 
    '''
    print('query', time.asctime())
    sim[0] = kw1_model.docvecs.most_similar([sim[0]])
    sim[1] = kw1_model.docvecs.most_similar([sim[1]])
    sim[2] = kw1_model.docvecs.most_similar([sim[2]])
    sim[3] = kw2_model.docvecs.most_similar([sim[3]])
    sim[4] = kw2_model.docvecs.most_similar([sim[4]])
    sim[5] = kw2_model.docvecs.most_similar([sim[5]])
    sim[6] = kw3_model.docvecs.most_similar([sim[6]])
    sim[7] = kw3_model.docvecs.most_similar([sim[7]])
    sim[8] = kw3_model.docvecs.most_similar([sim[8]])
    print('query', time.asctime())

    '''
    All of the index-similarity pairs will be form into a dictionary with index as key and similarity as value.
    As there may be same index but different similarity returned via different model.
    Therefore, the value list will be stored in this dictionary, and an average of similarity will got later.
    '''
    dict_id = {}
    for i in sim:
        for (key, val) in i:
            if dict_id.get(key + 1):
                dict_id[key + 1].append(val)
            else:
                dict_id[key + 1] = [val]


    '''
    compute the average of similarity and store in a new dict. 
    '''
    res = {}
    for key, val in dict_id.items():
        if (len(val) > 2):
        #    res[key] = sum(val) / len(val)
            if (len(val) == 9):
                res[key] = sum(val) / len(val)
            else:
                #add one at denominator can reduce the weight of which only has been returned a few times
                res[key] = sum(val) / (len(val) + 1)

    res = sorted(res.items(), key=lambda item: item[1], reverse=True)

    queid = [dt.query_cquestion_by_id(id) for (id, _) in res]#query the question id via index
    quess = [dt.get_title_by_queId(id.question_id) for id in queid]#query the title of question via question id
    res = [dt.get_answer_by_queId(id.question_id) for id in queid]#query the answers of question via question id

    res = [sorted(i, key= lambda x: x.score, reverse=True) for i in res]#sort the answers by thier score

    '''form the list into the dict and return'''
    res_dict = {}
    for index, i in enumerate(quess):
        if len(res[index]):
            for ans in res[index]:
                if ans.answers:
                    res_dict[i.title] = ans.answers
                    break
        if len(res_dict) == 3: break

    return res_dict
