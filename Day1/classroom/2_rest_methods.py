from flask import Flask
app =Flask('__name__')

@app.route("/",methods=["GET"])
def hello_get():
    return "<p> hello Get</p>"


@app.route("/",methods=["POST"])
def hello_post():
    return "<p> hello post</p>"


@app.route("/",methods=["PUT"])
def hello_put():
    return "<p> hello put</p>"


@app.route("/",methods=["PATCH"])
def hello_patch():
    return "<p> hello patch</p>"


@app.route("/",methods=["DELETE"])
def hello_delete():
    return "<p> hello Delete</p>"