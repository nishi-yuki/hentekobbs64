#! /usr/bin/env python3

from bottle import route, run, template, redirect, request, response
import json
import time
import sys

import randkanjiname

# @route("/hello/<name>")
# def hello(name):
#     return template("<b>Hello {{name}}</b>!", name=name)

comments = []
users = {}
preuse_names = randkanjiname.make_namelist()


@route("/")
def index():
    # return template("board.html", comments=comments)
    return template("board.html")


@route("/postcomment", method="POST")
def ajax_sended():
    t = request.forms.getunicode("t")
    if not t:
        return
    userid = request.get_cookie("id")
    print(userid)
    if (not userid) or (userid not in users):
        print("[INFO] New user")
        userid = str(time.time())
        response.set_cookie("id", userid)
        users[userid] = {"name": preuse_names.pop()}

    comments.append("[{}]: {}".format(users[userid]['name'], t))
    return "success"


@route("/getcomments", method="GET")
def returnt():
    return json.dumps(comments)

if __name__ == "__main__":
    hostname = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    run(host=hostname, port=8080)
