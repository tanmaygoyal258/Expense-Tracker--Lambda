#consider today to be 2021-06-19

import sqlite3 as db
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def view_by_category(category):
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql1 = '''
    select * from expenses where category = '{}'
    '''.format(category)
    results = pd.read_sql_query(sql1,conn)
    print(results)
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
    results = pd.read_sql_query(sql1,conn)#
    print(results)
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

def graph_by_dates(date1,date2):
    conn = db.connect("expenses.db")
    sql = '''
    select * from expenses where date between '{}' and '{}'
    '''.format(date1,date2)
    df = pd.read_sql_query(sql,conn)
    x = df.groupby('category')['amount'].sum()
    plt.subplot(1,2,1)
    x.plot(kind = 'bar')
    plt.subplot(1,2,2)
    x.plot(kind = 'pie' , label ="")
    plt.show()


def graph_by_category(category):
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = '''
    select * from expenses where category = '{}'
    '''.format(category)
    df = pd.read_sql_query(sql,conn)
    print(df.sort_values('date'))
    df.plot(kind='bar', x = 'date', y= 'amount')
    plt.title("Overall")
    plt.show()
    new = df['date'].str.split("-" , expand = True)
    df['year'] = new[0]
    x = df.groupby('year')['amount'].sum()
    plt.subplot(1,2,1)
    x.plot(kind = 'bar')
    plt.title("Yearly")
    plt.subplot(1,2,2)
    x.plot(kind = 'pie' , label ="")
    plt.title("Yearly")
    plt.show()
    
def row_count():
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = '''
    select * from expenses
    '''
    cur.execute(sql)
    results = cur.fetchall()
    return len(results)   

init()
init_values()
view_all()
#view_by_category("education")
#view_by_date("2020-08-25", "2020-08-25")
#graph_by_dates("2020-01-01" , "2020-12-31")
#graph_by_category("health and personal care")
#graph_by_category("education")

