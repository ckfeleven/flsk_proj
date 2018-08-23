# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 20:51:50 2018

@author: Joanne
"""

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
SelectField, IntegerField, DecimalField, DateField)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Project, Team
from datetime import date

#from wtforms_sqlalchemy.fields import QuerySelectField

from wtforms.ext.sqlalchemy.fields import QuerySelectField


#from wtforms.fields.html5 import DateField

#from flask_login import current_user
#from wtforms.ext.sqlachemy.fields import QuerySelectField

class LoginForm(FlaskForm):
     username = StringField('Username', validators=[DataRequired()])
     password = PasswordField('Password', validators=[DataRequired()])
     remember_me = BooleanField('Remember Me')
     submit = SubmitField('Sign In')
     
def proj_list():
    return Project.query  


    
class MiniForm(FlaskForm):
     username = StringField('Username', validators=[DataRequired()])
     date = DateField('Date', default = date.today)
     #project = SelectField('Project', choices=[('project1', 'project1'), ('project2','project2')])
     project = QuerySelectField(query_factory = proj_list, get_label='project')
     task = SelectField('Task', choices=[('task1', 'task1'), ('task2', 'task2'), ('task3', 'task3')])
     predicted_hrs = DecimalField('Predicted Hours')
     actual_hrs = DecimalField('Actual Hours')
     submit = SubmitField('Submit')
     
def team_list():
    return Team.query
     
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    team = QuerySelectField(query_factory = team_list, get_label='team')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SearchForm(FlaskForm):
    date = StringField('Date', default = date.today)
    submit = SubmitField('Submit')
    
