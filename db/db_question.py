# created by z5089986 

from datetime import datetime
import pandas as pd
import db.database as db
from db.database import Question
from db.database import base


class DBQue():


    def __init__(self):
        self.que = Question()

    def get_keywords_all(self, count=0):
        '''
        Connect to the Question Table, return query result
        :param count: the number of rows will be returned.
        :return:a list of object of Question class, containing only value of keyword column, which is the result of query

        '''
        if count:
            data_lines = Question.query.with_entities(Question.keywords).limit(count).all()
            return data_lines
        else:
            return Question.query.with_entities(Question.keywords).all()

    def upload_db(self, csv_path = "../dataset/Questions.csv"):

        '''
        load the data from the file and update to the database
        :param csv_path: string, file path
        :return: None
        '''

        csv_file = pd.read_csv(csv_path, encoding="ISO-8859-1", usecols=["Id", "Title", "Body"])

        exist_data = self.get_all_queId()
        exist_data = set([i.question_id for i in exist_data])

        del_list = []
        _ = [del_list.append(i) for i in csv_file.index if int(csv_file.ix[i, "Id"]) in exist_data]

        csv_file = csv_file.drop(index=del_list)
        csv_file = pd.DataFrame(csv_file).reset_index()

        #as the orginal question detail is HTML form, it should be clean by using format_question function
        body_line = csv_file['Body'].apply(db.format_question).values.tolist()
        title_line = csv_file['Title'].values.tolist()


        with open("../data/body_line.txt", 'w', encoding='utf-8') as file:
            processing = [file.write(line.strip(' ').strip('\n')+'\n') for line in body_line]
        print("--------------------to words-----------------------")

        #key words extraction
        body_words = db.build_dictionary(lines=body_line, freq=0)
        title_words = db.build_dictionary(lines=title_line, freq=0)


        for i, row in enumerate(csv_file.index):
            item = tuple(csv_file.ix[row, ["Id", "Title"]])
            model = Question(question_id=int(item[0]), title=str(item[1]).strip(), update_time=datetime.now(), questions=','.join(body_words[i]), keywords=','.join(title_words[i]))
            base.session.add(model)
            if (i+1)%1000==0: print(i+1)
        base.session.commit()

    def update_keywords_all(self):
        '''
        update keyword colunms
        :return:
        '''
        data_lines = self.query_all()
        title_list = [i.title for i in data_lines]

        data_words = db.build_dictionary(lines=title_list, freq=0)
        max = len(data_words)
        for i, j in  enumerate(data_lines):
            print(i)
            j.keywords = ','.join(data_words[i])
        base.session.commit()

    def update_nltkkeywords_all(self):
        '''
        update nltkwords colunms
        :return:
        '''
        data_lines = self.query_all()
        title_list = [i.title for i in data_lines]
        print("-----to word-----")
        data_words = list(db.sent_nltk_word(title_list))

        print("-----to word complete-----")
        max = len(data_words)
        for i, j in  enumerate(data_lines):
            print("----------{}--------".format(i))
            j.nltkwords = ','.join(data_words[i])
        base.session.commit()

    def query_all(self, count=0):
        '''
        Connect to the Question Table, return query result
        :param count: the number of rows will be returned.
        :return:a list of object of Question class, which is the result of query

        '''
        if count:
            data_lines = Question.query.limit(count).all()
            return data_lines
        else:
            data_lines = Question.query.all()
            return data_lines

    def get_questions(self, count=0):
        '''
        Connect to the Question Table, return query result
        :param count: the number of rows will be returned.
        :return:a list of object of Question class, which is the result of query

        '''
        if count:
            data_lines = Question.query.limit(count).all()
            return data_lines
        else:
            return Question.query.all()

    def get_question_by_queId(self, queId):
        '''
        Connect to the Question Table, return query result via question id
        :param queId: a single question id input.
        :return: a single object of Question class, which is the result of query

        '''
        return  Question.query.filter_by(question_id = queId).first()

    def get_title_by_queId(self, queId):
        '''
        Connect to the Question Table, return query result via question id
        :param queId: a single question id input.
        :return: a single object of Question class, containing only the value of title column, which is the result of query

        '''
        return  Question.query.with_entities(Question.title).filter_by(question_id = queId).first()

    def get_keywords_by_queId(self, queId):
        '''
        Connect to the Question Table, return query result via question id
        :param queId: a single question id input.
        :return: a single object of Question class, containing only the value of keywords column, which is the result of query

        '''
        return  Question.query.with_entities(Question.keywords).filter_by(question_id = queId).first()


    def get_all_queId(self):
        '''
        Connect to the Question Table, return query result
        :return:a list of object of Question class, containing only value of question_id column, which is the result of query

        '''
        data_lines = Question.query.with_entities(Question.question_id).all()
        return data_lines

    def query_by_queId(self, id=0):
        '''
        Connect to the Question Table, return query result via question id
        :param id: a single question id input.
        :return: a single object of Question class, which is the result of query

        '''
        data_lines = Question.query.filter_by(question_id=id).first()
        return data_lines

    def query_by_id(self, id=0):
        '''
        Connect to the Question Table, return query result via id
        :param id: a single id input.
        :return: a single object of Question class, which is the result of query

        '''
        return  Question.query.get(id)


    def delete_by_id(self, id=0):
        '''
        Connect to the Question Table, delete the row via id.
        :param id: a single id input.
        :return: None
        '''
        data_line = self.query_by_id(id)
        base.session.delete(data_line)
        base.session.commit()
