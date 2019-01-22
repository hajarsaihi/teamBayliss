from wtforms import Form, StringField, SelectField

class KinaseSearchForm(Form):
    choices = [('Kinase', 'Kinase'), ('Family', 'Family')]
    select = SelectField('Search for Kinase:', choices=choices)
    search = StringField('')
