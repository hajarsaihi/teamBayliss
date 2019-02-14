### Import required packages!
import os
from app import app
from flask import Flask, Markup, render_template, flash,url_for, render_template, request, redirect,g,send_from_directory, Response, request, send_file
from forms import KinaseSearchForm, PhosphositeSearchForm, InhibitorSearchForm
from models import Kinase_Information, Kinase_Phosphosite, inhibitor_information
from db_setup import init_db, db_session
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
#import matplotlib.pyplot as plt
#import datetime
import re
import requests
###############################################################################


init_db() #initialise the database

###############################################################################
@app.route("/") #define homepage route
def index():
  return render_template("index.html")

###### Kinase #################################################################
@app.route('/kinase', methods=['GET', 'POST'])
def kinase():
    search = KinaseSearchForm(request.form) # import search form and run a request
    if request.method == 'POST': # if the user is searching for information (ie posting a searchstring to retrieve data)
        return k_search_results(search) # run the kinase search function
    return render_template('kinase.html', form=search)

@app.route('/k_search_results')
def k_search_results(search):
    results = []
    search_string = search.data['search'] # search string given the user input data

    if search_string:
        if search.data['select'] == 'Protein Kinase Name': # check if protein kinase name was selected
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.kinase.ilike(search_string)) #qry the database for kinase information
            #use ilike for case sensitive search
            results = qry.all() # output all the query results

            iqry = db_session.query(Kinase_Information, inhibitor_information)\
                    .filter(Kinase_Information.kinase.ilike(search_string))\
                    .join(inhibitor_information, Kinase_Information.kinase == inhibitor_information.target1) # run a join query to find out inhibitors
            inhibresults = iqry.all()

            pqry = db_session.query(Kinase_Information, Kinase_Phosphosite)\
                    .filter(Kinase_Information.kinase.ilike(search_string))\
                    .join(Kinase_Phosphosite, Kinase_Information.kinase == Kinase_Phosphosite.gene)
            phosphresults = pqry.all() # run a join query to find out kinase substrates
            phosphresults.sort()


        elif search.data['select'] == 'Alias Name': # check if alias name was selected
            #search_string = search_string.upper()
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.Alias.contains(search_string)) # query alias names
            results = qry.all()

        elif search.data['select'] == 'Gene Name': # check if gene name was selected
            qry = db_session.query(Kinase_Information).filter(Kinase_Information.gene_name.ilike(search_string))# query matching gene name
            results = qry.all()

    if not results: # if no results were found..
        flash('No results found!') #.. flash the error message
        return redirect('/kinase') # and return back to kinase search

    elif search.data['select'] == 'Alias Name': # if the user selected Alias ..
	    return render_template('alias.html', results=results) # .. direct them to the alias page

    else:
        # display results
        return render_template('kinase_results.html', results=results, inhibresults=inhibresults, phosphresults=phosphresults) # render the kinase results page


@app.route('/kinase/<kinase>') # for the internal hyperlink a kinase profile route is defined, and the <kinase> is queried as before.
def profile(kinase):
    qry = db_session.query(Kinase_Information).filter(Kinase_Information.kinase.ilike(kinase))

    iqry = db_session.query(Kinase_Information, inhibitor_information).filter(Kinase_Information.kinase.ilike(kinase))\
              .join(inhibitor_information, Kinase_Information.kinase == inhibitor_information.target1) # use join query to find information about inhibitors

    pqry = db_session.query(Kinase_Information, Kinase_Phosphosite).filter(Kinase_Information.kinase.ilike(kinase))\
              .join(Kinase_Phosphosite, Kinase_Information.kinase == Kinase_Phosphosite.gene) # use join query to find information on protein substrate
    results = qry.all()
    inhibresults = iqry.all()
    phosphresults = pqry.all()
    return render_template('kinase_results.html', results=results, inhibresults=inhibresults, phosphresults=phosphresults)# render the kinase results page

###### Inhbitor ###############################################################
@app.route('/Inhibitor', methods=['GET', 'POST'])
def Inhibitor():
    search = InhibitorSearchForm(request.form)
    if request.method == 'POST':
        return i_search_results(search)# run the inhibitor search function if the method is POST
    return render_template('Inhibitor.html', form=search)

@app.route('/i_search_results')
def i_search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == ' ChEMBL ID ':
            qry = db_session.query(inhibitor_information).filter(inhibitor_information.chembl_ID.ilike(search_string)) # search for chembl ID that is
            # same as the search string - use ilike for case sensitive search
            results = qry.all()

        elif search.data['select'] == 'GSK Name':

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
        return render_template('inhib_results.html', results=results)

@app.route('/inhbitor/<chembl>') # for the internal hyperlink an inhibitor profile route is defined, and the <chembl> is queried as before.
def inhibprofile(chembl):
    qry = db_session.query(inhibitor_information).filter(inhibitor_information.chembl_ID.ilike(chembl))
    results = qry.all()
    return render_template('inhib_results.html', results=results) # render the inhibitor results page

###### Phosphosites ###########################################################
@app.route('/Phosphosite', methods=['GET', 'POST'])
def Phosphosite():
    search = PhosphositeSearchForm(request.form)
    if request.method == 'POST':
        return p_search_results(search)# run the phosphosite search function if the method is POST
    return render_template('Phosphosite.html', form=search)

@app.route('/Phosphosite results')
def p_search_results(search):
    results = {}
    search_string = search.data['search']
    data_obj = db_session.query(Kinase_Phosphosite).filter(Kinase_Phosphosite.substrate_protein.ilike(search_string)).first()

    if  data_obj: # if there is a query
        results['substrate'] = data_obj.substrate_protein
        results['gene'] = data_obj.gene
        results['loc'] = data_obj.genomic_location
        results['acc_id'] = data_obj.sub_accession
    return render_template('phosph_results.html', result=results) # render the phosphorylation results page

@app.route('/substrate/<sub>') # for the internal hyperlink a substrate profile route is defined, and the <sub> is queried as before.
def substrateprofile(sub):
    results = {}
    qry = db_session.query(Kinase_Phosphosite).filter(Kinase_Phosphosite.substrate_protein.ilike(sub)).first()
    if  qry:
        results['substrate'] = qry.substrate_protein
        results['gene'] = qry.gene
        results['loc'] = qry.genomic_location
        results['acc_id'] = qry.sub_accession
    return render_template('phosph_results.html', result=results) # render the phosphorylation results page

###############################################################################
###TOOLS ###

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

ALLOWED_EXTENSIONS= set(['tsv'])   #only tsv files are allowed

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/Tool/", methods=['GET','POST'])
def Tool():
    return render_template('Tool.html')      #The upload button is shown

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


@app.route("/Tool/upload/compute/", methods=['POST'])

def plot():

    FC_P= request.form['FC_P']
    FC_P=float(FC_P)          # the numbers can be decimals therefore they have been specified  to be floats
    PV_P=request.form['PV_P']
    PV_P=float(PV_P)
    if request.form['CV_P'] == "":       #if the user does not provide with  CV_P value then the default would be 10.0
        CV_P=float(10)
    else:
        CV_P=request.form['CV_P']      #if the user does provide with a CV_P value then it will be used.
        CV_P=float(CV_P)

    N_P= request.form['N_P']         #The background noise threshold value will filter out all relative kinase activities according to this threshold.
    N_P=float(N_P)
    Inhibitor=request.form['Inhibitor']


    import relative_kinase6

    filename="./static/temp.tsv"


    input_data=relative_kinase6.open_file(filename)
    data=relative_kinase6.filter_data(input_data, FC_P, PV_P, CV_P, N_P)  #C6
    data=relative_kinase6.add_sub_gene(data)
    #print(data)
    DATAFRAME=relative_kinase6.database_retriever("final_data.db")

    data=relative_kinase6.add_kinase(data, "kinase.csv")
    #print(data)
    plot1=relative_kinase6.makeplot(data, FC_P, PV_P, Inhibitor)
    #print(data)
    plot2=relative_kinase6.makeplot_2(data, FC_P, PV_P, Inhibitor)

    script1, div1 =components(plot1)  # to get the data points(script1 & scrip2) and the javascript for the graph (div1 & div2)
    script2, div2 =components(plot2)

    data=relative_kinase6.pv_filter(data,PV_P) #C  #filter out data above PV_P, and rows with no kinases
   # print(data)
    Kinasetable_sorted=relative_kinase6.relative_kinase_activity_calculation(data)

    data_html=relative_kinase6.make_html(Kinasetable_sorted)  #to create a html format for teh website
    data_csv=relative_kinase6.make_csv(Kinasetable_sorted) #to create a csv file


###To get he java script of the Bokeh volcano plot, to ensure the link is dynamic and changes with the newer version of Bokeh that's why these are added here
     #CDN: Content Delivery Network

    cdn_js=CDN.js_files[0]   #Only the first link is used

    #To get the CSS style sheet of the Bokeh volcano plot
    cdn_css=CDN.css_files[0] #Only the first link is used


    return render_template("plot.html",

        FC_P =FC_P,
        PV_P=PV_P,
        CV_P=CV_P,
        Inhibitor=Inhibitor,
        script1=script1,
        div1=div1,
        script2=script2,
        div2=div2,
        cdn_css=cdn_css,
        cdn_js=cdn_js,
        Kinasetable_sorted=Kinasetable_sorted,
        data_html=data_html,
        data_csv=data_csv)
    return send_file('static/relative_kinase_activity.csv',
                     mimetype='text/csv',
                     attachment_filename='relative_kinase_activity.csv',
                     as_attachment=True)

###############################


if __name__ == "__main__":
  app.run(debug=True)
