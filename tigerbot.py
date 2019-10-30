#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import google_dialogflow
import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
from tornado.options import define, options, parse_command_line
import app.reply as reply

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class RecordHandler(tornado.web.RequestHandler):
    def post(self):
        # received a json message {'question': what is int? 'answer': answer1}
        question = self.get_argument("question")
        answer = self.get_argument("answer")
        displayname = self.get_argument('ques')
        print(question)
        print(answer)

        google_dialogflow.create_intent(displayname, [question], [answer])

        reply_json = {'msg': 'Thanks for your help to improve our system'}
        self.write(reply_json)


class ReplyHandler(tornado.web.RequestHandler):

    def generate_replay_msg(self, question):
        #  Generate a reply message from google_dialogflow or training model
        df_intent, df_text = google_dialogflow.get_response(google_dialogflow.get_analyzed_text_response(question))
        if (df_intent == 'Default Fallback Intent'):
            reply_msg = 'from training model'
        else:
            reply_msg = df_text
        return reply_msg

    # Return the reply message to front end.
    def post(self):
        question = self.get_argument("question")
        reply_msg = self.generate_replay_msg(question)
        show_hints = "no"
        dict_test = {}
        if reply_msg == 'from training model':
            show_hints = "yes"
            dict_test = reply.reply(question)

        reply_json = {"reply_msg": reply_msg, "reply_other": dict_test, "show_hints": show_hints}
        self.write(reply_json)


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/message/new", ReplyHandler),
            (r"/message/record", RecordHandler)

        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
