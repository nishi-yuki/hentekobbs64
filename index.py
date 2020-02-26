#! /usr/bin/env python3

from bottle import route, run, template, redirect, request, response
import json
import time
import sys

import dbclient

# @route("/hello/<name>")
# def hello(name):
#     return template("<b>Hello {{name}}</b>!", name=name)
MAX_COMMENT_LENGTH = 256
TOO_LONG_MSG = '(長いのでカットしました)'


@route("/")
def index():
    # return template("board.html", comments=comments)
    return template("board.html")


@route("/comments", method="POST")
def ajax_sended():
    t = request.forms.getunicode("t")
    comment = t[:MAX_COMMENT_LENGTH]
    if len(t) > MAX_COMMENT_LENGTH:
        comment += TOO_LONG_MSG
    if not comment:
        return
    userid = request.get_cookie("id")
    print('userid:', userid)
    try:
        userid = dbclient.save_comment(userid, comment)
    except dbclient.UsersTableAlreadyFull:
        dbclient.init_tables()
        userid = dbclient.save_comment(userid, comment)
    response.set_cookie("id", str(userid))
    return "success\n"


@route("/comments", method="GET")
def returnt():
    result = dbclient.get_comments()
    comments = ['[{}]: {}'.format(i['name'], i['comment']) for i in result]
    return json.dumps(comments)


if __name__ == "__main__":
    hostname = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    run(host=hostname, port=8080)
