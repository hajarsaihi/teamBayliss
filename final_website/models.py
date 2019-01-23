from app import db

class Kinase_Information(db.Model):
    """"""
    __tablename__ = "Kinase_Information"

    kinase = db.Column('Name', db.String, primary_key = True)
    family = db.Column('Family', db.String)
    subFamily = db.Column('Subfamily', db.String)
    entrez = db.Column('Entrez_GeneID', db.String)
    Alias = db.Column('Alias', db.String)
    location = db.Column('location', db.String)

class Inhibitor_Information(db.Model):
    """"""
    __tablename__ = "Inhibitor_Information"

    chembl_ID = db.Column('ChEMBL_ID', db.Integer, primary_key = True)
    name = db.Column('Name', db.String)
    syn = db.Column('Synonyms', db.String)
    mol_formula = db.Column('Molecular_Formula', db.String)
    type = db.Column('Type', db.String)

class Kinase_Phosphosite(db.Model):
    """"""
    __tablename__ = "Kinase_Phosphosite"

    chembl_ID = db.Column('ChEMBL_ID', db.Integer, primary_key = True)
    name = db.Column('Name', db.String)
    syn = db.Column('Synonyms', db.String)
    mol_formula = db.Column('Molecular_Formula', db.String)
    type = db.Column('Type', db.String)
