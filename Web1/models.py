from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_data.db'
db = SQLAlchemy(app)

class Kinase_Information(db.Model):
    __tablename__ = 'Kinase_Information'
    kinase = db.Column('Kinase_Name', db.Unicode, primary_key = True)
    family = db.Column('Family', db.Unicode)
    subFamily = db.Column('SubFamily', db.Unicode)
    entrez = db.Column('ENTREZ_GENEID', db.Unicode)
    location = db.Column('Location', db.Unicode)

class Phosphosites(db.Model):
    __tablename__ = 'Kinase_Phosphosite'
    Phosphosite_ID = db.Column('Kinase_Name', db.Integer, primary_key = True)
    gene = db.Column('Family', db.Unicode)
    chr_loc = db.Column('HU_CHR_LOC', db.Unicode)
    mod_res = db.Column('MOD_RSD', db.Unicode)
    accession = db.Column('ACC_ID', db.Unicode)
    site_seq = db.Column('SITE_SEQ', db.Unicode)
