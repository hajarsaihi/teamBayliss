from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_data.db'
app.secret_key = '_Hdjghdgsdf495/'
db = SQLAlchemy(app)
