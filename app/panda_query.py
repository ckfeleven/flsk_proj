# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:59:12 2018

@author: Joanne
"""

import pandas as pd
from pandas import DataFrame, Series
import sqlalchemy as sql
import json
import datetime
from sqlalchemy import func
from sqlalchemy.sql import label
from app import app, db
from app.models import Minicard

engine = sql.create_engine('sqlite:///E:\\Documents\\Dropbox\\py_proj\\flsk_proj\\app.db')

df = pd.read_sql_table('minicard', engine)

#print(df.describe())

grouped = df[['username', 'predicted_hrs', 'date']].query('date == 20180829').groupby([df['username'], df['task']]).sum()


jdf = grouped.reset_index().to_json(orient = 'columns')

ddf = grouped.reset_index().to_dict(orient = 'list')

this_day = datetime.datetime.now()

a_date = datetime.datetime.strptime('2018-09-05', '%Y-%m-%d')

year_week = a_date.strftime("%Y-%W")

first_day = datetime.datetime.strptime(year_week + '-1', "%Y-%W-%w")

days = ['-1', '-2', '-3', '-4', '-5']

[(datetime.datetime.strptime(year_week + x, "%Y-%W-%w")) for x in days]

def daze(x):
    days_list = ['-1', '-2', '-3', '-4', '-5']
    target_date = datetime.datetime.strptime(x, '%Y-%m-%d')
    week_num = target_date.strftime("%Y-%W")
    return [(datetime.datetime.strptime(week_num + day, "%Y-%W-%w").strftime('%Y-%m-%d')) for day in days_list]
    
def taskz(x, y):
    #task_list = ['Task1', 'Task2', 'Task3']
    result = db.session.query(Minicard, label('total_hrs', func.sum(Minicard.actual_hrs))).group_by(Minicard.task).filter(Minicard.date == x).filter(Minicard.task == y).all()
    return result

datetime.datetime.strptime
#[datetime.datetime.strptime(year_week + x, "%Y-%W-%w"), for x in days]
#group_mean = grouped.sum()

def taskz(x, y):
    try:
        result = db.session.query(Minicard, label('total_hrs', func.sum(Minicard.actual_hrs))).group_by(Minicard.task).filter(Minicard.date == x).filter(Minicard.task == y).all()
        a = result[0][1]
    except IndexError:
        return 0
    return a

[[taskz(y, x) for x in ['task1', 'task2', 'task3']] for y in ['2018-09-01', '2018-09-02', '2018-09-03']]

