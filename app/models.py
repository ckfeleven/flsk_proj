# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 08:28:54 2018

@author: Joanne
"""

from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    team = db.Column(db.String, db.ForeignKey('team.team')) 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username) 
        
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
        
class Minicard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(64))
    date = db.Column(db.Date)
    #date = db.Column(db.String(64))
    project = db.Column(db.String(64))
    task = db.Column(db.String(64))
    subtask = db.Column(db.String(64))
    predicted_hrs = db.Column(db.Numeric)
    actual_hrs = db.Column(db.Numeric)
        
        
    def __repr__(self):
        return '<Minicard {}>'.format(self.username) 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Team(db.Model):
    team = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return '<Team {}>'.format(self.team)

    
class Project(db.Model):
    project = db.Column(db.String, primary_key=True)

    #def __repr__(self):
    #    return '<Project {}>'.format(self.project)
        
    def __repr__(self):
        return self.project
        

        
class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task = db.Column(db.String(64))
    children = db.relationship("Tasks")    
    
    def __repr__(self):
        #return '<Task {}>'.format(self.task)
        return self.task
    
