# created by z5089986 

from db.database import Ansewr


class DBAns():

    def __init__(self):
        self.ans = Ansewr()


    def query_all(self, count=0):
        '''
        Connect to the Answer Table, return query result
        :param count: the number of rows will be returned.
        :return:a list of object of Answer class, which is the result of query

        '''
        if count:
            data_lines = Ansewr.query.limit(count).all()
            return data_lines
        else:
            data_lines = Ansewr.query.all()
            return data_lines

    def get_ANS_by_queId(self, queId):
        '''
        Connect to the Answer Table, return query result via question id.
        :param queId: a single question id input.
        :return: a single object of Answer class, containing only score and answers' detail, which is the result of query
        '''
        data_lines = Ansewr.query.with_entities(Ansewr.score, Ansewr.answers).filter_by(question_id=queId).all()
        return data_lines
