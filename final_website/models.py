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

class inhibitor_information(db.Model):
    """"""
    __tablename__ = "inhibitor_information"

    chembl_ID = db.Column('ChEMBL_ID', db.Integer, primary_key = True)
    name = db.Column('Name', db.String)
    syn = db.Column('Synonyms', db.String)
    mol_formula = db.Column('Molecular_Formula', db.String)
    type = db.Column('Type', db.String)

class Kinase_Phosphosite(db.Model):
    """"""
    __tablename__ = "Kinase_Phosphosite"

    keys_row = db.Column('Keys_row', db.Integer, primary_key = True)
    gene = db.Column('GENE', db.Integer)
    pkinase = db.Column('KINASE', db.String)
    kinase_accession = db.Column('KIN_ACC_ID', db.String)
    substrate_protein = db.Column('SUBSTRATE', db.String)
    sub_gene = db.Column('SUB_GENE', db.String)
    sub_accession = db.Column('SUB_ACC_ID', db.String)
    Phosphosite = db.Column('SITE_7_AA', db.String)
