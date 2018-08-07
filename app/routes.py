# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 20:47:02 2018

@author: Joanne
"""
from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, MiniForm, RegistrationForm, SearchForm
from app.models import Minicard, User
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.tables import Results
from sqlalchemy import func
from sqlalchemy.sql import label
from datetime import date

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Craig'}
    
    posts = [
        {
            'author' : {'username' : 'John'},
            'body' : 'Beautiful day in Portland'        
        },
        {
             'author' : {'username' : 'Karen'},
             'body' : 'The avengers movie was so cool!'        
        }
    
    ]    
    
    
    
    return render_template('index.html',title = 'Home', posts=posts)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    
    return render_template('search.html', title = 'Search', form=search) 
    
@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['date']
 
    #if search.data['date'] != '':
    qry = db.session.query(Minicard).filter(Minicard.date == search_string)
    results = qry.all()
 
    if not results:
        flash('No results found!')
        return redirect('/search')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
        
#db.session.query(Minicard.username, label('total_hrs', func.sum(Minicard.predicted_hrs))).group_by(Minicard.username).all()
    
@app.route('/minicard', methods=['GET', 'POST'])
def minicard():
    form = MiniForm()
    
    if request.method == 'POST':
    
        minicard = Minicard()
        save_changes(minicard, form)
        return redirect('/minicard')
    #if form.validate_on_submit():
    #    flash('Login requested for user {}, remember_me={}'.format(
    #        form.username.data, form.remember_me.data))
    #    return redirect('/index')
    return render_template('minicard.html', title = 'Minicard', form=form)
   
   
def save_changes(minicard, form):
    minicard.username = form.username.data
    minicard.date = form.date.data
    minicard.project = form.project.data
    minicard.task = form.task.data
    minicard.predicted_hrs = form.predicted_hrs.data
    minicard.actual_hrs = form.actual_hrs.data
    
    db.session.add(minicard)
    
    db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app .route('/simple_chart')
def chart():
    sum_data = db.session.query(Minicard.username, label('total_hrs', func.sum(Minicard.predicted_hrs))).group_by(Minicard.username).filter(Minicard.date == date.today()).all()
    legend = 'Daily data'
    #labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August']
    #values = [10, 9, 8, 7, 6, 4, 7, 8]
    labels = [x[0] for x in sum_data]
    values = [x[1] for x in sum_data]
    return render_template('chart.html', values=values, labels=labels, legend=legend)
    
@app .route('/simple_chart2')
def chart2():
    return render_template('chart2.html')
    
@app.route('/item/<int:id>', methods =  ['GET', 'POST'])
def edit(id):
    qry = db.session.query(Minicard).filter(Minicard.id == id)
    result = qry.first()
    
    if result:
        form = MiniForm(formdata=request.form, obj = result)
        if request.method == 'POST':
            save_changes(result, form)
            flash('Minicard updated sucessfully')
            return redirect(url_for('search'))
        return render_template('edit_minicard.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
