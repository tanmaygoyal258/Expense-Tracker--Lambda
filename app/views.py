from flask import render_template, redirect, request
from app import app

import sqlite3 as db

def init():
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists expenses(
    date date,
    category string,
    amount real,
    additional_comments string
    )
    '''
    cur.execute(sql)
    conn.commit()


def insert(date, category, price, comm):
    conn = db.connect("expenses.db")
    cur = conn.cursor()

    sql= '''
    INSERT INTO expenses VALUES('{}','{}',{},'{}')
    '''.format(date, category, price, comm)

    cur.execute(sql)
    conn.commit()

def view_all():
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql1 = '''
    select * from expenses
    '''
    results = pd.read_sql_query(sql1,conn)
    print(results)
    sql2 = '''
    select sum(amount) from expenses
    '''
    cur.execute(sql2)
    total = cur.fetchone()
    print("\n Total expense  = {}".format(total[0]))
    return results, total[0]

def init_values():
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = '''
    select * from expenses
    '''
    cur.execute(sql)
    results = cur.fetchall()
    if len(results)==0:
        insert("2021-06-19", "rent" , 20000, "")
        insert("2021-06-19" , "transport", 2345,"")
        insert("2021-06-19", "groceries" , 3450,"")
        insert("2021-06-19" , "home and utilities" , 1247 , "")
        insert("2021-06-19", "insurance" , 125000, "")
        insert("2021-06-19" , "bills and emi" , 11230 , "")
        insert("2021-06-19" , "education" , 150000,"")
        insert("2021-06-19" , "health and personal care" , 6700 , "")
        insert("2021-05-23", "rent" , 15000, "")
        insert("2021-05-19" , "transport", 1345,"")
        insert("2021-05-25", "groceries" , 2324,"")
        insert("2021-05-14" , "home and utilities" , 908 , "")
        insert("2021-05-11", "insurance" , 150000, "")
        insert("2021-05-18" , "bills and emi" , 4560 , "")
        insert("2021-05-12" , "education" , 29000,"")
        insert("2021-05-20" , "health and personal care" , 3700 , "")
        insert("2020-02-14", "rent" , 20000, "")
        insert("2020-08-25" , "transport", 2345,"")
        insert("2020-05-07", "groceries" , 3450,"")
        insert("2020-04-02" , "home and utilities" , 1247 , "")
        insert("2020-08-26", "insurance" , 125000, "")
        insert("2020-07-22" , "bills and emi" , 11230 , "")
        insert("2020-09-13" , "education" , 150000,"")
        insert("2020-01-25  " , "health and personal care" , 6700 , "")
        insert("2020-05-14" , "health and personal care" , 3400 , "")
    conn.commit()

def delete(date, price):
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql= '''
   DELETE from expenses where date = '{}'
    '''.format(date)

    cur.execute(sql)
    conn.commit()

def row_count():
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = '''
    select * from expenses
    '''
    cur.execute(sql)
    results = cur.fetchall()
    return len(results)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/new',methods = ['GET' , 'POST'])
def new():
    return render_template("form.html")

@app.route ('/submit' , methods = ['GET' , 'POST'])  
def submit():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']
    comment = request.form['comment']
    old_row = row_count()
    insert(date,category,amount,comment)
    new_row = row_count()
    if new_row - old_row ==1:
        message = "Entry successful"
    else:
        message = "Entry unsuccessful. Please Try again!"

    return render_template("action_page.html" ,
                            date = date , 
                            category = category,
                            amount = amount,
                            message = message)