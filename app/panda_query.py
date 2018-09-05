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

engine = sql.create_engine('sqlite:///E:\\Documents\\Dropbox\\py_proj\\flsk_proj\\app.db')

df = pd.read_sql_table('minicard', engine)

#print(df.describe())

grouped = df[['username', 'predicted_hrs', 'date']].query('date == 20180829').groupby([df['username'], df['task']]).sum()


jdf = grouped.reset_index().to_json(orient = 'columns')

ddf = grouped.reset_index().to_dict(orient = 'list')
#group_mean = grouped.sum()

