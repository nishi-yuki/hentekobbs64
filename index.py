#! /usr/bin/env python3

from bottle import route, run, template, redirect, request

# @route("/hello/<name>")
# def hello(name):
#     return template("<b>Hello {{name}}</b>!", name=name)

comments = []

def comments_html_gen():
    return "<br>".join(comments)

@route("/")
def index():
    return template("board.html", comments=comments)

@route("/postcomment", method="POST")
def ajax_sended():
    t = request.forms.getunicode("t")
    comments.append(t)
    return comments_html_gen()

# @route("/return", method="POST")
# def returnt():
#     t = request.forms.getunicode("t")
#     print(type(t))
    
#     "安全"
#     return template('あなたが送った文章は "{{t}}" です．', t=t)

#     "危険! XSSされるよ"
#     # return f"""<!DOCTYPE html>
#     #     <body>
#     #     あなたが送った文章は {t} です
#     #     </body>
#     # </html>"""


run(host="localhost", port=8080)
