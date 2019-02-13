from app import db

class Kinase_Information(db.Model):
    """"""
    __tablename__ = "Kinase_Information"

    kinase = db.Column('Name', db.String, primary_key = True)
    family = db.Column('Family', db.String)
    subFamily = db.Column('Subfamily', db.String)
    entrez = db.Column('Entrez_GeneID', db.String)
    full_name= db.Column('Entrez_description', db.String)
    Alias = db.Column('Alias', db.String)
    uniprot = db.Column('uniprot_IDs', db.String)
    location = db.Column('location', db.String)
    gene_name = db.Column('gene_name', db.String)
    accID = db.Column('uni_accession', db.String)

class inhibitor_information(db.Model):
    """"""
    __tablename__ = "inhibitor_information"

    chembl_ID = db.Column('ChEMBL_IDs', db.Integer, primary_key = True)
    name = db.Column('Name', db.String)
    syn = db.Column('Synonyms', db.String)
    mol_formula = db.Column('Molecular_Formula', db.String)
    type = db.Column('Type', db.String)
    image = db.Column("image_link", db.String)
    target1 = db.Column('TARGETS_1', db.String)
    target2 = db.Column('TARGETS_2', db.String)
    inchi = db.Column('INCHI', db.String)
    smiles = db.Column('SMILES', db.String)
    maxphase = db.Column('Max_Phase', db.String)
    aromaticrings = db.Column('Aromatic_Rings', db.String)
    structuretype = db.Column('Structure_Type', db.String)

    bioactivities = db.Column('Bioactivities', db.String)
    alogP = db.Column('AlogP', db.String)
    psa = db.Column('PSA', db.String)
    hba = db.Column('HBA', db.String)
    hbd = db.Column('HBD', db.String)
    rotatablebonds = db.Column('Rotatable_Bonds', db.String)
    passesro3 = db.Column('Passes_Ro3', db.String)
    qed = db.Column('QED_Weighted', db.String)
    apka = db.Column('ACD_ApKa', db.String)
    bpka = db.Column('ACD_BpKa', db.String)
    acdlogp = db.Column('ACD_LogP', db.String)
    acdlogd = db.Column('ACD_LogD', db.String)
    heavyatoms = db.Column('Heavy_Atoms', db.String)
    molweightmono = db.Column('Molecular_Weight_Monoisotopic', db.String)


class Kinase_Phosphosite(db.Model):
    """"""
    __tablename__ = "Kinase_Phosphosite"

    keys_row = db.Column('Key_rows', db.Integer, primary_key = True)
    gene = db.Column('GENE', db.Integer)
    pkinase = db.Column('KINASE', db.String)
    kinase_accession = db.Column('KIN_ACC_ID', db.String)
    substrate_protein = db.Column('SUBSTRATE', db.String)
    sub_gene = db.Column('SUB_GENE', db.String)
    sub_accession = db.Column('SUB_ACC_ID', db.String)
    # the following is a quick last minute solution to retrieving phosphosites (only the first 15) and we recognise another more efficient approach is better but due to time
    # constraints and finding this problem very late it is the only solution.
    s1 = db.Column('Z_SITE_1', db.String)
    s2 = db.Column('Z_SITE_2', db.String)
    s3 = db.Column('Z_SITE_3', db.String)
    s4 = db.Column('Z_SITE_4', db.String)


#Kinase_Information.kinase = relationship(inhibitor_information,primaryjoin=inhibitor_information.target1==Kinase_Information.kinase)
db.create_all()
