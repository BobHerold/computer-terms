import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_terms")
def get_terms():
    terms = mongo.db.terms.find().sort("term", 1)
    return render_template("terms.html", terms=terms)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    terms = mongo.db.terms.find({"$text": {"$search": query}})
    return render_template("terms.html", terms=terms)


@app.route("/add_term", methods=["GET", "POST"])
def add_term():
    if request.method == "POST":
        term = {
            "term": request.form.get("term"),
            "definition": request.form.get("definition")
        }
        mongo.db.terms.insert_one(term)
        flash("Term Successfully Added")
        #return redirect(url_for("get_terms"))
    return render_template("add_term.html")


@app.route("/edit_term/<term_id>", methods=["GET", "POST"])
def edit_term(term_id):
    term = mongo.db.terms.find_one({"_id": ObjectId(term_id)})
    return render_template("edit_term.html", term=term)

 
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)