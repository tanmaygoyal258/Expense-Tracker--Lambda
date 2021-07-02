from flask import render_template, redirect, request
from app import app

import sqlite3 as db
import pandas as pd

global view_by

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
    cur.execute(sql1)
    results = cur.fetchall()
    #results = pd.read_sql_query(sql1,conn)
    #print(results)
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

def view_by_category(category):
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql1 = '''
    select * from expenses where category = '{}'
    '''.format(category)
    cur.execute(sql1)
    results = cur.fetchall()
    #results = pd.read_sql_query(sql1,conn)
    #print(results)
    sql2 = '''
    select sum(amount) from expenses
    '''
    cur.execute(sql2)
    total = cur.fetchone()
    print("\n Total expense  = {}".format(total[0]))
    sql3 = '''
    select sum(amount) from expenses where category = '{}'
    '''.format(category)
    cur.execute(sql3)
    total_category = cur.fetchone()
    print("\n Total expense in the category = {}".format(total_category[0]))
    return results, total[0], total_category[0]

def view_by_date(date1,date2):
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql1 = '''
    select * from expenses where date between '{}' and '{}'
    '''.format(date1, date2)
    cur.execute(sql1)
    results = cur.fetchall()
    #results = pd.read_sql_query(sql1,conn)
    #print(results)
    sql2 = '''
    select sum(amount) from expenses
    '''
    cur.execute(sql2)
    total = cur.fetchone()
    print("\n Total expense  = {}".format(total[0]))
    sql3 = '''
    select sum(amount) from expenses where date between '{}' and '{}'
    '''.format(date1, date2)
    cur.execute(sql3)
    total_category = cur.fetchone()
    print("\n Total expense in between these dates = {}".format(total_category[0]))
    return results , total[0], total_category[0]


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

@app.route("/view", methods = ['GET' , 'POST'])
def view():
    return render_template("view_database.html")


@app.route("/view_c_or_d", methods = ['GET' , 'POST'])
def view_c_or_d():
    view_by = request.form['view']
    if view_by == 'view all': return redirect("/view_all_results")
    elif view_by=="view by category": return redirect("/view_category_choice")
    else: return redirect("/view_date_choice")


@app.route("/view_all_results" , methods = ['GET' , 'POST'])
def view_all_results():
        results , total = view_all()
        return render_template("view_result_data.html" , results = results , total = total)

@app.route("/view_category_choice" , methods = ['GET' , 'POST'])
def view_category_choice():
        return render_template("view_database.html" ,opt=2)

@app.route("/view_date_choice" , methods = ['GET' , 'POST'])
def view_date_choice():
        return render_template("view_database.html" ,opt=3)


@app.route("/view_category_results" , methods = ['GET' , 'POST'])
def view_category_results():    
        category = request.form['view_category']
        results , total , total_c = view_by_category(category)
        return render_template("view_result_data.html" , results = results , total = total, 
                                                            total_c = total_c)
@app.route("/view_date_results" , methods = ['GET' , 'POST'])
def view_date_results():
        date1 = request.form['from']
        date2 = request.form['to']
        results , total , total_c = view_by_date(date1, date2)
        return render_template("view_result_data.html" , results = results , total = total, 
                                                            total_c = total_c)
