import os
from app import app
from flask import Flask, Markup, render_template, flash,url_for, render_template, request, redirect,g,send_from_directory, Response, request
from forms import KinaseSearchForm, PhosphositeSearchForm, InhibitorSearchForm
from models import Kinase_Information, Kinase_Phosphosite, inhibitor_information
from db_setup import init_db, db_session
from tables import KResults, IResults, PResults
import pandas as pd
import numpy as np
import csv
import pandas as pd
from werkzeug.utils import secure_filename
from bokeh.plotting import figure,  ColumnDataSource, output_notebook, show
from bokeh.resources import CDN, INLINE
from bokeh.embed import file_html, components
from bokeh.models import HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool, SaveTool
from bokeh.palettes import brewer
import matplotlib.pyplot as plt
import datetime
import re
import requests
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
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Substrate':
            #search_string = search_string.upper() use ilike for case sensitive search
            qry = db_session.query(Kinase_Phosphosite).filter(Kinase_Phosphosite.sub_gene.ilike(search_string))
            results = qry.all()

        else:
            qry = db_session.query(Kinase_Phosphosite)
            results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/Phosphosite')

    else:
        # display results
        return render_template('phosph_results.html', results=results)
###############################################################################
###TOOLS ###

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

ALLOWED_EXTENSIONS= set(['tsv'])   #only tsv files are allowed 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/Tool/", methods=['GET','POST'])
def Tool():
    return render_template('Tool.html')

@app.route("/Tool/upload", methods=['POST'])
def upload():
#the name of the input is file in the html
        target = os.path.join(UPLOAD_FOLDER, 'static/')    #to create a folder into which the file will be saved
        print(target)

        if not os.path.isdir(target):                  #if folder is not made it should be made
            os.mkdir(target)

        for file in request.files.getlist("file"):
            filename = secure_filename(file.filename)
            print(file)
            filename =file.filename
            destination ="/".join([target, "temp.tsv"])   #saves teh file as temp.tsv
            print(destination)
            file.save(destination)

        return render_template("Upload.html")
     

###Output where the volcano plot and table will be shown 
@app.route("/Tool/upload/compute", methods=['POST'])

def plot():
    import Userdata_script

    Userdata_script.open_file(file)
    
    Userdata_script.process_query()

    Userdata_script.cv_filter(dd, CV_P)
    Userdata_script.makeplot(dd, FC_P, PV_P, Inhibitor)



    return render_template("plot.html", 
        script1=script1,
        div1=div1,
        script2=script2,
        div2=div2,
        cdn_css=cdn_css,
        cdn_js=cdn_js,
        Kinasetable_sorted=Kinasetable_sorted )


###############################


@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  app.run(debug=True)
