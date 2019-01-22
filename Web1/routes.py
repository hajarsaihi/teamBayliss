from flask import Flask, render_template
#from models import db

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/gl/Documents/Bioinformatics/Scripts/01_InProgress/Web1/Database_Construction/PROTEIN_KINASE_DATABASE_DRAFT_1.db'
#app.config['SQLALCHEMY_BINDS'] = { }

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/ProteinKinase")
def ProteinKinase():
  return render_template("ProteinKinase.html")

@app.route("/Inhibitor")
def Inhibitor():
  return render_template("Inhibitor.html")

@app.route("/Phosphosite")
def Phosphosite():
  return render_template("Phosphosite.html")

@app.route("/Tool")
def Tool():
  return render_template("Tool.html")

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  app.run(debug=True)