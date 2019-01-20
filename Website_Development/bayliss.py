from flask import Flask, render_template, url_for, redirect
import pandas as pd

# import libraries needed create and process forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__) 

app.config['SECRET_KEY']= '83d6024507165be8dc84384369ee8e6e'      #This secure key was takebn by running Python by installing 'pip install python2-secrets' and then 'import secrets' then typing in: secrets.token_hex(16)


#The routes are defined 
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/proteinkinase")
def proteinkinase():
    return render_template('proteinkinase.html', title='Protein Kinase')


@app.route("/proteinkinaseinhibitors")
def proteinkinaseinhibitors():
    return render_template('proteinkinaseinhibitors.html', title='Protein Kinase Inhibitors')


#So that changes can be made while the website is still running. 
if __name__ == '__main__':
	app.run(debug=True)