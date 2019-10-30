# created by z5089986 

import app.tagDoc2vec as tagd2v
from app.dataset import Dataset

dts = Dataset()

#fetch all question key words from database
questions = dts.query_cquestion()

#extract the labels of each question
labels = [str(i.label).split(',') for index, i in enumerate(questions)]

#extract the question id of each question
idlist = [i.question_id for i in questions]

#fetch the question from database by question id
questions = dts.get_questions_by_ids(idlist)

#package the labels and key words in a tuple, form into a list.
keywords = [(labels[index],str(i.keywords).split(',')) for index, i in enumerate(questions)]
print("--------file loaded---------")


for i in range(20, 36, 5):
    print("-------start epoch {} training----------".format(i))
    #call the model training function
    tagd2v.run(keywords, filename="keyword", epcho=i)
