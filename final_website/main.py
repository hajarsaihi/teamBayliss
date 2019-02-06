from app import app
from flask import Flask, render_template, flash, render_template, request, redirect
from forms import KinaseSearchForm, PhosphositeSearchForm, InhibitorSearchForm
from models import Kinase_Information, Kinase_Phosphosite, inhibitor_information
from db_setup import init_db, db_session
from tables import KResults, IResults, PResults
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
        return k_search_results(search)
    return render_template('kinase.html', form=search)

@app.route('/k_search_results')
def k_search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Protein Kinase Name':
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.kinase.ilike(search_string))
            results = qry.all()

        elif search.data['select'] == 'Alias Name':
            search_string = search_string.upper()
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.Alias.contains(search_string))
            results = qry.all()

        elif search.data['select'] == 'Gene Name':
            search_string = search_string.upper()
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.gene_name.ilike(search_string))
            results = qry.all()

        else:
            qry = db_session.query(Kinase_Information)
            results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/kinase')

    else:
        # display results
        table = KResults(results)
        table.border = True
        return render_template('kinase_results.html', results=results)

@app.route('/profile/<kinase>')
def profile(kinase):
    qry = db_session.query(Kinase_Information).filter(Kinase_Information.kinase.ilike(kinase))
    results = qry.all()
    return render_template('profile.html', results=results)

###### Inhbitor ###############################################################
@app.route('/Inhibitor', methods=['GET', 'POST'])
def Inhibitor():
    search = InhibitorSearchForm(request.form)
    if request.method == 'POST':
        return i_search_results(search)
    return render_template('Inhibitor.html', form=search)

@app.route('/i_search_results')
def i_search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == ' ChEMBL ID ':
            #search_string = search_string.upper() use ilike for case sensitive search
            qry = db_session.query(inhibitor_information).filter(inhibitor_information.chembl_ID.ilike(search_string))
            results = qry.all()

        elif search.data['select'] == 'GSK Name':
            #search_string = search_string.upper() use ilike for case sensitive search
            qry = db_session.query(inhibitor_information).filter(inhibitor_information.name.ilike(search_string))
            results = qry.all()

        else:
            qry = db_session.query(inhibitor_information)
            results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/Inhibitor')

    else:
        # display results
        table = IResults(results)
        table.border = True
        return render_template('inhib_results.html', results=results)

###### Phosphosites ###########################################################
@app.route('/Phosphosite', methods=['GET', 'POST'])
def Phosphosite():
    search = PhosphositeSearchForm(request.form)
    if request.method == 'POST':
        return p_search_results(search)
    return render_template('Phosphosite.html', form=search)

@app.route('/Phosphosite results')
def p_search_results(search):
    import csv
    results = {}
    search_string = search.data['search']
    # csv_file = csv.reader(open('Locations.csv', "rb"), delimiter=",")
    csvFile = 'Locations.csv'
    reader = csv.reader(open(csvFile, 'r'))

    for data in reader:
        if data[1].lower() == search_string.lower():
            results['subtract'] = data[1]
            results['gene'] = data[0]
            results['loc'] = data[3]
            results['acc_id'] = data[2]
            break

    # if search_string:
    #     if search.data['select'] == 'Substrate':
    #         #search_string = search_string.upper() use ilike for case sensitive search
    #         qry = db_session.query(Kinase_Phosphosite).filter(Kinase_Phosphosite.sub_gene.ilike(search_string))
    #         results = qry.all()
    #
    #     else:
    #         qry = db_session.query(Kinase_Phosphosite)
    #         results = qry.all()

    # if not results:
    #     flash('No results found!')
    #     return redirect('/Phosphosite')
    #
    # else:
    #     # display results
    return render_template('phosph_results.html', result=results)
###############################################################################

@app.route("/Tool")
def Tool():
  return render_template("Tool.html")

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  app.run(debug=True)
