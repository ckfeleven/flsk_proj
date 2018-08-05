# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 07:21:22 2018

@author: Joanne
"""

from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('Id', show=False)
    timestamp = Col('Timestamp', show=False)
    username = Col('Username')
    date = Col('Date')
    project = Col('Project')
    task = Col('Task')
    predicted_hrs = Col('Predicted Hours')
    actual_hrs = Col('Actual Hours')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))