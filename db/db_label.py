# created by z5089986 

from datetime import datetime
import pandas as pd
from db.database import base
from db.database import Label

class DBLabel():


    def __init__(self):
        self.lab = Label()

    def upload_db(self, csv_path = "../dataset/Tags.csv"):
        '''
        load the data from the file and update to the database
        :param csv_path: string, file path
        :return: None
        '''

        csv_file = pd.read_csv(csv_path, encoding="ISO-8859-1")


        csv_file = csv_file.drop(columns=["Id"])
        csv_file["count"] = 1
        data_lines = pd.DataFrame(csv_file.groupby(["Tag"]).sum()).sort_index(by="count", axis=0, ascending=False)

        max = len(data_lines)
        time=0
        for row in data_lines.index:

            model = Label(label=row, update_time=datetime.now())
            base.session.add(model)
            time += 1
            print(time)
        base.session.commit()

    def query_all(self, count=0):
        '''
        Connect to the Label Table, return query result
        :param count: the number of rows will be returned.
        :return:a list of object of Label class, which is the result of query

        '''

        if count:
            data_lines = Label.query.limit(count).all()
            return data_lines
        else:
            data_lines = Label.query.all()
            return data_lines


    def query_by_id(self, id=0):
        '''
        Connect to the Label Table, return query result via id.
        :param id: a single id input.
        :return: a single object of Label class, which is the result of query
        '''
        return Label.query.get(id)

    def delete_by_id(self, id=0):
        '''
        Connect to the Label Table, delete the row via id.
        :param id: a single id input.
        :return: None
        '''
        data_line = self.query_by_id(id)
        base.session.delete(data_line)
        base.session.commit()
