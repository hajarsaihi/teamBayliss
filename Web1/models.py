from app import db

class Kinase_Information(db.Model):
    """"""
    __tablename__ = "Kinase_Information"

    kinase = db.Column('Kinase_Name', db.String, primary_key = True)
    family = db.Column('Family', db.String)
    subFamily = db.Column('SubFamily', db.String)
    entrez = db.Column('ENTREZ_GENEID', db.String)
    location = db.Column('Location', db.String)

class Phosphosites(db.Model):
    __tablename__ = "Kinase_Phosphosite"
    
    Phosphosite_ID = db.Column('Kinase_Name', db.Integer, primary_key = True)
    gene = db.Column('Family', db.String)
    chr_loc = db.Column('HU_CHR_LOC', db.String)
    mod_res = db.Column('MOD_RSD', db.String)
    accession = db.Column('ACC_ID', db.String)
    site_seq = db.Column('SITE_SEQ', db.String)
