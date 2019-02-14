
# Team Bayliss - QMUL MSc Bioinformatics
# PhosphoKinase: Software Group Development Project

Phospho Kinase was developed by Bayliss – a group of 4 students that are part of the MSc Bioinformatics Programme at Queen Mary University of London, under the supervision of Professor Conrad Bessant and Dr Fabrizio Smeraldi.

Phospho Kinase explores the functional annotation of phosphosites and functional description of protein kinases, the key controllers of cell behavior. We focus the full complement of protein kinases in any sequenced genome through a functional Kinase search engine. The kinase search engine is connected to an extensive database of Kinases including classification and kinase information. In addition, phospho kinase provides information about all phosphosites phosphorylated by all kinases across a platform of proteins. 


## Website Link

http://bayliss.eu-west-2.elasticbeanstalk.com/ 

## Getting Started

To run on your localhost please download the directory 'final_website'. 

Once downloaded please open and run the 'final_database_friha.py' to create and populate the database called 'final_data.db'.


### The packages required

Python 3.6.0 <br/>
requests==2.21.0 <br/>
bokeh==1.0.4 <br/>
Flask==1.0.2 <br/>
flask_sqlalchemy==2.3.2 <br/>
flask_table==0.5.0 <br/>
matplotlib==3.0.2 <br/>
numpy==1.16.1 <br/>
pandas==0.24.1 <br/>
SQLAlchemy==1.2.17 <br/>
Werkzeug==0.14.1 <br/>
WTForms==2.2.1 <br/>
ipython==7.2.0 <br/>

To install these:
```
pip install requests==2.21.0 
pip install bokeh
pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-Table
pip install matplotlib
pip install numpy
pip install pandas
pip install SQLAlchemy
pip install Werkzeug
pip install WTForms
pip install ipython

```

### Running the website

In your commandline open the 'final_website' directory and run the following command:

```
python main.py
```

Copy the localhost URL and paste it into your browser (for best user experience please use Mozilla Firefox or Google Chrome).

This would lead you to the homepage of 'Phospho Kinase', where you can browse 'Kinase', 'Inhibitors', 'Phosphosites' and 'PP Tool'. 


## Authors

* **Friha Zafar** - [FrihaZ](https://github.com/FrihaZ) & [FrihaZa](https://github.com/FrihaZa) 
* **Hajar Saihi** - [startswithH](https://github.com/startswithH)
* **Gabriel Lim** - [W K G Lim](https://github.com/gabelim)
* **Omer Baskan** - [Omer Baskan](https://github.com/omerbaskan)

See also the list of [contributors] (https://github.com/startswithH/teamBayliss/graphs/contributors) who participated in this project.


## Acknowledgments

* Thank you to Professor Conrad Bessant and Dr Fabrizio Smeraldi for your support.


