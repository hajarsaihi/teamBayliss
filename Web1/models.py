from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Protein_Kinase(db.Model):
  uid = db.Column(db.Integer, primary_key = True)


 # def __init__(self, firstname, lastname, email, password):
    #self.firstname = firstname.title()
   # self.lastname = lastname.title()
    #self.email = email.lower()
    #self.set_password(password)
     
  #def set_password(self, password):
    #self.pwdhash = generate_password_hash(password)

  #def check_password(self, password):
    #return check_password_hash(self.pwdhash, password)