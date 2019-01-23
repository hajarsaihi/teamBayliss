from flask import Flask, render_template, flash, render_template, request, redirect
from forms import KinaseSearchForm
from forms import InhibitorSearchForm
from models import Kinase_Information
from app import app
from db_setup import init_db, db_session
from tables import KResults
###############################################################################

app = Flask(__name__)
app.secret_key = 'ca/i4tishfkaSJSF'
init_db()
###############################################################################
@app.route("/")
def index():
  return render_template("index.html")

###### Kinase #################################################################
@app.route('/kinase', methods=['GET', 'POST'])
def kinase():
    search = KinaseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('kinase.html', form=search)

@app.route('/Kinase results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Kinase':
            #search_string = search_string.upper() use ilike for case sensitive search
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.kinase.ilike(search_string))
            results = qry.all()

        elif search.data['select'] == 'Family':
            search_string = search_string.upper()
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.family.ilike(search_string))
            results = qry.all()

        elif search.data['select'] == 'Alias Name':
            search_string = search_string.upper()
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.Alias.contains(search_string))
            results = qry.all()

        else:
            qry = db_session.query(Kinase_Information)
            results = qry.all()
    else:
        flash('Search Field Empty')
        return redirect('/kinase')

    if not results:
        flash('No results found!')
        return redirect('/kinase')

    else:
        # display results
        table = KResults(results)
        table.border = True
        return render_template('kinase_results.html', table=table)

###### Inhbitor ###############################################################
@app.route('/Inhibitor', methods=['GET', 'POST'])
def Inhibitor():
    search = InhibitorSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('Inhibitor.html', form=search)

@app.route('/Inhibitor results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'CHEMBL ID':
            #search_string = search_string.upper() use ilike for case sensitive search
            qry = db_session.query(HERE).filter(HERE.kinase.ilike(search_string))
            results = qry.all()

        else:
            qry = db_session.query(Kinase_Information)
            results = qry.all()
    else:
        flash('Search Field Empty')
        return redirect('/kinase')

    if not results:
        flash('No results found!')
        return redirect('/kinase')

    else:
        # display results
        table = IResults(results)
        table.border = True
        return render_template('inhib_results.html', table=table)

###### Phosphosites ###############################################################
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
