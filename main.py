from flask import Flask,request,render_template,redirect,url_for,session,flash
import datalogger
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'troulilol21'
log = datalogger.Logger()
app.permanent_session_lifetime = timedelta(minutes=10)

@app.errorhandler(405)
def page_not_found(e):
    #snip
    return redirect(url_for('index')), 405

@app.errorhandler(404)
def page_not_found(e):
    #snip
    return """<h1>I think you are in a wrong way,</h1><a href="/">Main page</a>""", 404


@app.route("/",methods = ["GET"])
def index():
    result = log.flower("article")
    return render_template("index.html",len = len(result) ,datas = result)

@app.route("/new",methods = ["POST","GET"])
def new():
    if "user" in session:
        if request.method == "POST":
            titre = request.form["titre"]
            content = request.form["content"]
            log.insert('article',{'title':titre,'content':content,'poster':'Henri'})
            return redirect(url_for('index'))
        else:
            return render_template('add.html')
    else:
        flash('Vous n\'êtes pas connecté.')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)