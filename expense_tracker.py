#consider today to be 2021-06-19

import sqlite3 as db
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def graph_by_dates(date1,date2):
    conn = db.connect("expenses.db")
    sql = '''
    select * from expenses where date between '{}' and '{}'
    '''.format(date1,date2)
    df = pd.read_sql_query(sql,conn)
    x = df.groupby('category')['amount'].sum()
    x.plot(kind = 'bar')
    plt.title("Category Wise")
    plt.show()
    x.plot(kind = 'pie' , label ="")
    plt.title("Category Wise")
    plt.show()


def graph_by_category(category):
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = '''
    select * from expenses where category = '{}'
    '''.format(category)
    df = pd.read_sql_query(sql,conn)
    #print(df.sort_values('date'))
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


def graph_all():
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = '''
    select * from expenses 
    '''
    df = pd.read_sql_query(sql,conn)
    #print(df.sort_values('date'))
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
    x = df.groupby('category')['amount'].sum()
    x.plot(kind = 'bar')
    plt.title("Category Wise")
    plt.show()
    x.plot(kind = 'pie' , label ="")
    plt.title("Category Wise")
    plt.show()



#graph_by_dates("2020-01-01" , "2020-12-31")
#graph_by_category("health and personal care")
#graph_by_category("education")
#graph_all()
