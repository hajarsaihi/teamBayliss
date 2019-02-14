from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_data.db' # configurate the database and provide the relative path to the database
app.config['secret_key'] = 'ca/i4tishfkhaSJSF'
app.secret_key = '_Hdjghdgsdf495/'

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
