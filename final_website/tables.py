from flask_table import Table, Col

# Define tables for result output (for kinases, inhibitors, and phosphosites)
class KResults(Table):
    kinase = Col('Name')
    family = Col('Family')
    subFamily = Col('Subfamily')
    entrez = Col('Entrez_GeneID')
    location = Col('location')

class IResults(Table):
    chembl_ID = Col('ChEMBL_ID')
    name = Col('Name')
    syn = Col('Synonyms')
    mol_formula = Col('Molecular_Formula')
    type = Col('Type')

class PResults(Table):
    gene = Col('GENE')
    pkinase = Col('KINASE')
    kinase_accession = Col('KIN_ACC_ID')
    substrate_protein= Col('SUBSTRATE')
    sub_gene = Col('SUB_GENE')
    sub_accession = Col('SUB_ACC_ID')
    Phosphosite = Col('SITE_7_AA')
