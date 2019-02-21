#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Flask, Response, render_template, redirect, request
from werkzeug import secure_filename
import os, time, re
app = Flask(__name__)

@app.before_request
def check_domain():
    if not request.host in ["codality.hackers.moe", "xn--d3np-ooa.hackers.moe"]:
        return redirect("https://duckduckgo.com")

@app.after_request
def log_request(res):
    remote_addr = request.headers["X-Forwarded-For"] if "X-Forwarded-For" in request.headers else request.remote_addr
    line = "{1} - [{0}] \"{4} {2}\" {3} - UA: {5}".format(
        time.strftime("%y/%m/%d %H:%M:%S"),
        remote_addr,
        request.url.encode("utf-8"),
        res.status,
        request.method,
        request.headers["User-Agent"])
    print line
    return res

@app.route("/")
def index():
    return view_file("index.txt")

def command(command):
    import commands
    output = commands.getstatusoutput("cd content; %s" % command)[1]
    if command.split(" ")[0] == "ls": # will add broken links if not in "content/" directory
        output2 = ""
        for line in output.split("\n"):
            line = line.split(" ")
            if re.match("[rwxd-][rwx-]", line[0]):
                line[-1] = "<a href=\"/{0}\">{0}</a>".format(line[-1])
                line[2] = "hacker"
                line[3] = "hackers"
            line = " ".join(line)
            output2 += "{0}\n".format(line)
        output = output2
    if output[-1] == "\n": output = output[:-1]
    return output

def render(data):
    data = data.replace("$SIGNATURE", "d3npä")
    for cmd in re.findall(r'\$\((.*?)\)', data):
        data = data.replace("$(%s)" % cmd, command(cmd))
    data = data.replace("\\$", "$").replace("\\\\", "\\")
    return data

def guess_mime(filename):
    known_mimes = {"pdf" : "application/pdf", "mp4" : "video/mp4", "webm" : "video/webm"}
    extension = filename.split(".")[-1]
    if extension in known_mimes:
        return known_mimes[extension]
    return "text/plain"

@app.route("/<filename>")
def view_file(filename):
    if filename.split(".")[-1] in ["pdf", "mp3", "mp4"]:
        return redirect("/raw/" + filename)
    filename = secure_filename(filename)
    path = "content/" + filename
    if not os.path.exists(path):
        return Response(render_template("404.jinja", filename=filename), status=404)
    with open(path, "rb") as f:
        remote_addr = request.headers["X-Forwarded-For"] if "X-Forwarded-For" in request.headers else request.remote_addr
        res = Response(render_template("post.jinja", title=filename, content=f.read(), client_ip=remote_addr))
        res.headers["Content-Type"] = "text/html; charset=UTF-8"
        res.data = render(res.data)
        return res

@app.route("/raw/<filename>")
def view_raw_file(filename):
    path = "content/" + secure_filename(filename)
    if not os.path.exists(path):
        return Response(render_template("404.jinja", filename=filename), status=404)
    with open(path, "rb") as f:
        res = Response(f.read())
        res.headers["Content-Type"] = guess_mime(path) + "; charset=UTF-8"
        return res

@app.route("/css/<filename>")
def get_css(filename):
    path = "resources/css/" + secure_filename(filename)
    if not os.path.exists(path):
        return Response(render_template("404.jinja", filename=filename), status=404)
    with open(path, "rb") as f:
        res = Response(f.read())
        res.headers["Content-Type"] = "text/css; charset=UTF-8"
        return res

@app.route("/js/<filename>")
def get_js(filename):
    path = "resources/js/" + secure_filename(filename)
    if not os.path.exists(path):
        return Response(render_template("404.jinja", filename=filename), status=404)
    with open(path, "rb") as f:
        res = Response(f.read())
        res.headers["Content-Type"] = "text/javascript; charset=UTF-8"
        return res

@app.route("/ttf/<filename>")
def get_ttf(filename):
    path = "resources/ttf/" + secure_filename(filename)
    if not os.path.exists(path):
        return Response(render_template("404.jinja", filename=filename), status=404)
    with open(path, "rb") as f:
        res = Response(f.read())
        res.headers["Content-Type"] = "application/octet-stream; charset=UTF-8"
        return res

@app.route("/robots.txt")
def robots_txt():
    res = Response("User-agent: *\nDisallow: /", status=200)
    res.headers["Content-Type"] = "text/plain;"
    return res

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
