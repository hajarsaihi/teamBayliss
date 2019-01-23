from wtforms import Form, StringField, SelectField

class KinaseSearchForm(Form):
    choices = [('Kinase', 'Kinase'), ('Family', 'Family'), ('Alias Name', 'Alias Name')]
    select = SelectField('Search for Kinase:', choices=choices)
    search = StringField('')
