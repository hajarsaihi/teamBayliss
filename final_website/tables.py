from flask_table import Table, Col

class Results(Table):
    kinase = Col('Kinase_Name')
    family = Col('Family')
    subFamily = Col('SubFamily')
    entrez = Col('ENTREZ_GENEID')
    location = Col('Location')
