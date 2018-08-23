# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 20:49:43 2018

@author: Joanne
"""

from app import app, db
from app.models import User, Post, Minicard, Project, Team

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Minicard': Minicard, 'Project': Project, 'Team': Team}