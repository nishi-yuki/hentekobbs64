#! /usr/bin/env python3

from bottle import route, run, template, redirect, request
import json

# @route("/hello/<name>")
# def hello(name):
#     return template("<b>Hello {{name}}</b>!", name=name)

comments = []

def comments_html_gen():
    return "<br>".join(comments)

@route("/")
def index():
    # return template("board.html", comments=comments)
    return template("board.html")

@route("/postcomment", method="POST")
def ajax_sended():
    t = request.forms.getunicode("t")
    comments.append(t)
    return "success"


@route("/getcomments", method="GET")
def returnt():
    return json.dumps(comments)


run(host="localhost", port=8080)
