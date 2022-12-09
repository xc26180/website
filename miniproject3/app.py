from flask import Flask,render_template,request
import requests
import sqlite3
import pandas as pd
import os.path

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # turning the path to a absolute path
db_path = os.path.join(BASE_DIR, "mydb.db")

# add the data to a table in a sqlite3 database.
with sqlite3.connect(db_path) as con:                 
    con.execute("""CREATE TABLE IF NOT EXISTS Product
    (Category TEXT,
     Descriptions TEXT,
     Price INTEGER,
     Code TEXT);""")
    con.commit()


@app.route('/', methods=['GET','POST'])  # bind the URL for the home page function
def home():
    return render_template("home.html")

@app.route('/data', methods=['GET','POST']) # bind the URL for the Entering the Data function 
def data():
    return render_template("data.html")
   
@app.route('/result',methods=['GET','POST']) # bind the URL for collecting the data to dataframe function
def result():
    with sqlite3.connect('mydb.db') as con:
        if request.method == "POST":         # If the form has been submitted, then insert the values into the columns
            con.execute("INSERT INTO Product (Category,Descriptions,Price,Code) VALUES (:Category,:Descriptions,:Price,:Code)", request.form)    
        df = pd.read_sql("select * from Product", con)  # Select all columns in the pandas dataframe
        print(df)                            
        return render_template("home.html")
    

@app.route('/system', methods=['GET','POST']) # bind the URL for the retrieving the data page
def system():
    return render_template("system.html")

@app.route('/result2', methods=['GET','POST'])  # bind the URL for showing the table function
def result2():
    with sqlite3.connect('mydb.db') as con:
        if request.method == "POST":            # If the form has been submitted, then print the data received that matches the category the user asked in pandas dataframe.
            category = request.form.get('Category') 
            print(category)
            res = con.execute("SELECT * FROM Product WHERE Category = '%s'" %category)
            if not category or not len(list(res)): # If the category does not exist or the entry is empty, then shows the entire record
                print('Fail!')
                res = con.execute("SELECT * FROM Product")
                return render_template("result2.html", data = res)
            else:
                print('Success!')
                res = con.execute("SELECT * FROM Product WHERE Category = '%s'" %category)
                return render_template("result2.html",data = res)
app.run(debug = True,port=8080)
