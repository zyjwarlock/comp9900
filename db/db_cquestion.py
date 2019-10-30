# created by z5089986 

from datetime import datetime
import pandas as pd
from db.database import base
from db.database import Question
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db_tag import DBTag
from db.database import CQuestion

class DBCQue():

    labelset = set([(4, "pandas"), (6, "numpy"), (7,"list"), (8, "matplotlib"),
                    (9, "regex"), (10, "dictionary"), (12, "string"), (15,"csv"),
                    (16,"arrays"), (17, "json"), (42, "loops"), (31, "class"),
                    (35,"dataframe"), (36, "function"), (38, "file"),
                    (43, "scikit-learn"), (44, "pip"), (63, "import"), (65, "database"),
                    (85,"tuples"), (84,"matrix"), (148,"split"), (56, "for-loop"),(45, "algorithm"), (58, "sorting")])
    #labelset = set([(139, "while-loop"),(4734, "do-while"),(184, "set"),(869, "dataset"), (1186, "subset")])
    dict_label = {}


    def __init__(self):
        self.cque = CQuestion()

        for i in self.labelset:
            self.dict_label[i[0]] = i[1]

    def upload_db(self):
        '''
        update the CQuestion Table, via specific labels.
        :return: None
        '''

        dbTag = DBTag()

        for index, i in enumerate(list(self.dict_label.keys())):
            quelist = dbTag.get_questionId_by_label(i)
            print(index + 1, len(quelist))
            for j, queId in enumerate(quelist):
                cque = self.query_by_queId(queId)
                if(cque):
                    la_list = str(cque.label).split(',')
                    la_list.append(self.dict_label[i])
                    la_list = set(la_list)
                    cque.label = ','.join(la_list)
                else:
                    obj = CQuestion(question_id=queId, label=self.dict_label[i])
                    base.session.add(obj)
                if(j+1)%1000==0: print("finish: ", j + 1)
            base.session.commit()


    def query_by_id(self, id):
        '''
        Connect to the CQuestion Table, return query result via id
        :param id: a single id input.
        :return: a single object of CQuestion class, which is the result of query

        '''
        data = CQuestion.query.get(id)
        return data

    def query_by_queId(self, queId):
        '''
        Connect to the CQuestion Table, return query result via question id
        :param id: a single question id input.
        :return: a single object of CQuestion class, which is the result of query

        '''
        data = CQuestion.query.filter_by(question_id = queId).first()
        return data

    def query_all(self, count=0):
        '''
        Connect to the CQuestion Table, return query result
        :param count: the number of rows will be returned.
        :return:a list of object of CQuestion class, which is the result of query

        '''
        if count:
            data_lines = CQuestion.query.limit(count).all()
            return data_lines
        else:
            data_lines = CQuestion.query.all()
            return data_lines



