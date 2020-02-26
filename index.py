#! /usr/bin/env python3

from bottle import route, run, template, redirect, request, response
import json
import time
import sys

import dbclient

# @route("/hello/<name>")
# def hello(name):
#     return template("<b>Hello {{name}}</b>!", name=name)


@route("/")
def index():
    # return template("board.html", comments=comments)
    return template("board.html")


@route("/comments", method="POST")
def ajax_sended():
    t = request.forms.getunicode("t")
    if not t:
        return
    userid = request.get_cookie("id")
    print('userid:', userid)
    try:
        userid = dbclient.save_comment(userid, t)
    except dbclient.UsersTableAlreadyFull:
        dbclient.init_tables()
        userid = dbclient.save_comment(userid, t)
    response.set_cookie("id", str(userid))
    return "success"


@route("/comments", method="GET")
def returnt():
    result = dbclient.get_comments()
    comments = ['[{}]: {}'.format(i['name'], i['comment']) for i in result]
    return json.dumps(comments)


if __name__ == "__main__":
    hostname = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    run(host=hostname, port=8080)
