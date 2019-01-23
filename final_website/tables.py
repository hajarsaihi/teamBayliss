from flask_table import Table, Col

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
    chembl_ID = Col('ChEMBL_ID')
    name = Col('Name')
    syn = Col('Synonyms')
    mol_formula = Col('Molecular_Formula')
    type = Col('Type')
