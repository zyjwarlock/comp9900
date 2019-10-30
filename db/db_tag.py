# created by z5089986 

from datetime import datetime
import pandas as pd
from db.database import Tag
from db.db_label import DBLabel
from db.database import base

class DBTag():


    def __init__(self):
        self.tag = Tag()
        self.dblab = DBLabel()

    def upload_db(self, csv_path = "../dataset/Tags.csv"):

        '''
        load the data from the file and update to the database
        :param csv_path: string, file path
        :return: None
        '''

        csv_file = pd.read_csv(csv_path, encoding="ISO-8859-1")


        label = self.dblab.query_all()
        label_dict = {}
        for i in label: label_dict[str(i.label)] = i.id


        csv_file = csv_file.dropna(axis=0, how='any')

        tag_list = self.query_all()

        tag_list = set([i.question_id for i in tag_list])

        del_list = []

        _ = [del_list.append(i) for i in csv_file.index if int(csv_file.ix[i, "Id"]) in tag_list]
        csv_file = csv_file.drop(index=del_list)
        csv_file = pd.DataFrame(csv_file).reset_index()

        csv_file["label_id"] = csv_file["Tag"].apply(lambda x: label_dict[str(x)])




        max = len(csv_file)
        time=0
        for row in csv_file.index:
            item = tuple(csv_file.ix[row, ["Id", "label_id"]])

            model = Tag(question_id=int(item[0]), label_id=int(item[1]), update_time=datetime.now())
            base.session.add(model)
            time += 1
            if(time%10000 ==0 ):print(time)
        base.session.commit()

    def query_all(self, count=0):

        '''
        Connect to the Tag Table, return query result
        :param count: the number of rows will be returned.
        :return:a list of object of Tag class, which is the result of query

        '''

        if count:
            data_lines = Tag.query.limit(count).all()
            return data_lines
        else:
            data_lines = Tag.query.all()
            return data_lines

    def query_by_queId(self, id=0):
        '''
        Connect to the Tag Table, return query result via question id
        :param queId: a single question id input.
        :return: a list of objects of Question class, which is the result of query

        '''
        data_lines = Tag.query.filter_by(question_id=id).all()
        return data_lines

    def get_lableId_by_queId(self, id):
        '''
        Connect to the Tag Table, return query result via question id
        :param queId: a single question id input.
        :return: a list of objects of Tag class, containing only the value of label_id column, which is the result of query

        '''
        try:
            data_lines = Tag.query.with_entities(Tag.label_id).filter_by(question_id=id).all()
        except:
            print(id)
        return data_lines

    def get_label_by_queId(self, queId):
        '''
        Connect to the Tag Table and Label Table, return query result via question id
        :param queId: a single question id input.
        :return: a list of label of this question
        '''
        label_ids = self.get_lableId_by_queId(queId)
        res = [self.dblab.query_by_id(la.label_id) for la in label_ids]
        return [i.label for i in res]

    def get_questionId_by_label(self, labelid):
        '''
        Connect to the Tag Table, return query result via label id
        :param labelid: a single label id input.
        :return: a list of question id for which has this label
        '''
        tags = Tag.query.filter_by(label_id=labelid).all()
        questionId = [i.question_id for i in tags]
        return questionId

    def delete_by_id(self, id=0):
        '''
        Connect to the Tag Table, delete the row via id.
        :param id: a single id input.
        :return: None
        '''
        data_line = self.query_by_queId(id)
        base.session.delete(data_line)
        base.session.commit()
