from wtforms import Form, StringField, SelectField
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms import validators

# Create search forms for the three searches on the site
class KinaseSearchForm(Form):
    choices = [('Protein Kinase Name', 'Protein Kinase Name'), ('Alias Name', 'Alias Name')] # Define choices for the kinase search
    select = SelectField('Search for Kinase:', choices=choices) # the select field will include the choices defined
    search = StringField('',[validators.DataRequired()]) # this is a field that is empty that allows the user to search - a data required validator is added.

class InhibitorSearchForm(Form):
    choices = [(' ChEMBL ID ', ' ChEMBL ID '), ('GSK Name', 'GSK Name')]
    select = SelectField('Search for Inhibitor:', choices=choices)# Define choices for the inhibitor search
    search = StringField('',[validators.DataRequired()])# this is a field that is empty that allows the user to search - a data required validator is added.

class PhosphositeSearchForm(Form):
    choices = [('Substrate', 'Substrate')]# Define choices for the phosphosite search
    select = SelectField('Search for Phosphosite:', choices=choices)
    search = StringField('',[validators.DataRequired()])# this is a field that is empty that allows the user to search - a data required validator is added.
