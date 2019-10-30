# created by z5089986 

import json

from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
import app.reply as rp
from db.database import app
import os

api = Api(app,
          default = "cs9900", # Default namespace
          title = "Q&A Dataset", # Documentation Title
                  description = "This is cs9900 implementation." # Documentation Description
          )



qmodel = api.model("Question", {
    "question": fields.String
})

@api.route("/chatbot")
class reply(Resource):

    @api.response(200, "OK")
    @api.response(404, "error")
    @api.expect(qmodel, validate=True)

    def post(self):
        input = json.loads(request.data)
        question = input["question"]

        res = rp.reply(question)
        res_list = list(res.items())
        #data = qmodel.query.filter(qmodel.question_id == q_id).first()

        return {
                    'question_1': res_list[0],
                    'question_2': res_list[1],
                    'question_3': res_list[2]
                }, 200

fmodel = api.model("Filename", {
    "filename": fields.String
})

@api.route("/upload")
class upload(Resource):
    @api.response(200, "OK")
    @api.response(404, "error")
    @api.expect(fmodel, validate=True)
    def post(self):
        input = json.loads(request.data)
        filename = input["filename"]
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, filename)
        filename.save(upload_path)
        return {"message":""}, 200


if __name__ == '__main__':
     app.run()
