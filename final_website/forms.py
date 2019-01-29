from wtforms import Form, StringField, SelectField
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms import validators

class KinaseSearchForm(Form):
    choices = [('Protein Kinase Name', 'Protein Kinase Name'), ('Alias Name', 'Alias Name'),
                ('Gene Name', 'Gene Name')]
    select = SelectField('Search for Kinase:', choices=choices)
    search = StringField('',[validators.DataRequired()])

class InhibitorSearchForm(Form):
    choices = [(' ChEMBL ID ', ' ChEMBL ID '), ('GSK Name', 'GSK Name')]
    select = SelectField('Search for Inhibitor:', choices=choices)
    search = StringField('',[validators.DataRequired()])

class PhosphositeSearchForm(Form):
    choices = [('Substrate', 'Substrate')]
    select = SelectField('Search for Phosphosite:', choices=choices)
    search = StringField('',[validators.DataRequired()])
