from wtforms import Form, StringField, SelectField
class KinaseSearchForm(Form):
    choices = [('Kinase', 'Kinase'), ('Target', 'Target')]
    select = SelectField('Search for Kinase:', choices=choices)
    search = StringField('')
