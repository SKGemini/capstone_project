#from flask import Flask
#from flask import request, redirect, render_template, url_for, jsonify
#import pickle
#import pandas as pd
#from build_model import TextClassifier, get_data

from flask import Flask, render_template, request, flash, url_for, redirect
from wtforms import widgets, Form, validators, TextField, SubmitField, TextAreaField, StringField
from flask_table import Table, Col
from pymongo import MongoClient
#from flask_images import Images
#from bs4 import BeautifulSoup
#from isbntools.app import *

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
	book = TextField('Book',validators=[validators.required()])
	author = TextField('Author')
	isbn = TextField('ISBN')

# home page
@app.route('/')
def index():
    return render_template('jumbotron.html', title='Welcome!')

#about me page
@app.route('/about/')
def about():
    return render_template('about.html')

#project details page
@app.route('/project/')
def project():
    return render_template('project.html')

@app.route('/more/',methods = ['GET', 'POST'])
def form():
	image_url = None
	widget_html = None
	title = None
	author = None
	form = ReusableForm(request.form)
	if request.method == 'POST':
		book = request.form['book']
		author = request.form['author']
		isbn = request.form['isbn']

		if form.validate():
			flash('Thank you for your input!')
			collection = db.data
			search = collection.find_one({'title': book})
			if search:
				title = search['title']
				author = search['author']
				widget_html = widgets.HTMLString(''.join(search['widget']))
				image_url = search['image_url']
		else:
			flash('Error: Missing fields')

	return render_template('form.html',form=form,image=image_url,title=title,author=author,widget=widget_html)


if __name__ == '__main__':
	client = MongoClient()
	db = client['goodreads']
	app.run(host='0.0.0.0', port=8080, debug=True)
