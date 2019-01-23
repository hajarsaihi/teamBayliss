from flask_table import Table, Col

class Results(Table):
    kinase = Col('Name')
    family = Col('Family')
    subFamily = Col('Subfamily')
    entrez = Col('Entrez_GeneID')
    location = Col('location')
