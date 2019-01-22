from flask import Flask, render_template, flash, render_template, request, redirect
from forms import KinaseSearchForm
from models import Kinase_Information
from app import app
from db_setup import init_db, db_session
from tables import Results
###############################################################################

app = Flask(__name__)
app.secret_key = 'ca/i4tishfkaSJSF'
init_db()
###############################################################################

@app.route('/kinase', methods=['GET', 'POST'])
def kinase():
    search = KinaseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('kinase.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Kinase':
            search_string = search_string.upper()
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.kinase.contains(search_string))
            results = qry.all()

        elif search.data['select'] == 'Family':
            search_string = search_string.upper()
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.family.contains(search_string))
            results = qry.all()

        else:
            qry = db_session.query(Kinase_Information)
            results = qry.all()
    else:
        qry = db_session.query(Kinase_Information)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/kinase')

    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)

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
