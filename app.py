import sqlite3
import random
from flask import Flask, session, render_template, request, g

app = Flask(__name__)
# secret key is used to encrypt cookies
app.secret_key = "31xsyBa<VIt8]hD(q;<P18NYYaZyFh6qLeofB[ct"

@app.route("/", methods=["POST", "GET"])
def index():
    session["all_items"], session["shopping_items"] = get_db()
    return render_template("index.html",all_items = session["all_items"], shopping_items=session["shopping_items"])

# connect the sqlite database to the application
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('grocery_list.db')
        cursor = db.cursor()
        # select the name column from the groceries table
        cursor.execute("SELECT name FROM groceries")
        # get a list of all groceries from the table
        all_data = cursor.fetchall()
        # remove the tuple to return strings using list comprehension
        all_data = [str(val[0]) for val in all_data]
        
        # get initial list of 5 random grocery items
        shopping_list = all_data.copy()
        random.shuffle(shopping_list)
        shopping_list = shopping_list[:5]
    return all_data, shopping_list

@app.route("/add_items", methods=["POST"])
def add_items():
    session["shopping_items"].append(request.form["select_items"])
    session.modified = True
    return render_template("index.html",all_items=session["all_items"], shopping_items=session["shopping_items"])

@app.route("/remove_items", methods=["POST"])
def remove_items():
    checked_boxes = request.form.getlist("check")
    for item in checked_boxes:
        if item in session["shopping_items"]:
            idx = session["shopping_items"].index(item)
            session["shopping_items"].pop(idx)
            session.modified = True
    return render_template("index.html",all_items = session["all_items"], shopping_items=session["shopping_items"])

# terminate the database connection when done using it
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()