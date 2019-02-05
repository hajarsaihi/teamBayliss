
# coding: utf-8

# In[60]:



import pandas as pd
import numpy as np
import os
import re
import requests
from bokeh.plotting import figure, ColumnDataSource, output_notebook, show
from bokeh.models import HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool, SaveTool
from bokeh.palettes import brewer


#FC_P=float(input("Input Fold_Change Threshold")) #user input fold change parameter
#PV_P=float("Input pvalue Threshold") #user input fold change parameter
#CV_P=float("Input CV Thresholds") #user input fold change parameter
#Inhibitor=("Input inhibitor")  #user input fold change parameter

def open_file(filename):
    
#allow for user file input
# go through each file in the folder
#for file_name in os.listdir("."):
  # check if it ends with .tsv
    assert filename.endswith(".tsv")
    # open the file and process each line
    
    d = pd.read_csv(filename ,usecols=list(range(0,7)), na_values='inf', sep = '\t')
    return d

def filter_data(d, FC_P, PV_P, CV_P):


    d_cols=["Substrate", "Control_mean", "Inhibitor_mean", "Fold_change", "p_value", "ctrlCV", "treatCV" ]
    d.columns=d_cols

####drop out methonine and none####
    d=(d[~d.Substrate.str.contains("None")] ) #drop rows with "None"

    patternDel = r"\([M]\d+\)" #Use Regex to find "(M and any number of digits)" #\d+ : one or more digits)

    dd=(d[~d.Substrate.str.contains(patternDel)].copy()) #d1: rows with (Mddd) removed....copy() to remove conflict

#add split of gene/protein names to XXX_HUMAN   and (SNNN)

    dd[["Substrate","Phosphosite"]] = dd.Substrate.str.extract(r"(.+)\((.\d+)", expand=True)
    dd=cv_filter(dd, CV_P)
#
    return dd

#Function: Substrates with "_HUMAN" converted to Uniprot Gene Names
def convert_protein_name_to_gene_name(query):
    
    if re.match(r".+_HUMAN", query):
        URL = 'http://www.uniprot.org/uniprot/?query=' + query + '&columns=genes(PREFERRED)&format=tab'
        r = requests.get(URL)
        lines = r.text.split("\n")
        gene_name=lines[1:2]        #return top preferred uniprot gene result #get accession number
        
        return str(gene_name)  #return gene as string instead of string within a list [""] #get accession number
    else:
        return query



def add_sub_gene(dd):
#make copy of Substrate to Substrate gene

    dd["Sub_gene"]=dd["Substrate"].copy()
#Substrates with "_HUMAN" converted to Uniprot Gene Names
    dd.Sub_gene = dd.apply(lambda row: convert_protein_name_to_gene_name(row["Substrate"]), axis =1)
    dd["Sub_gene"] = dd["Sub_gene"].str.strip("[]").str.strip("''")  #remove square bracket and ''
      #remove square bracket and ''
#Removes Substrates "_HUMAN" with no Sub_gene result: likely experimental protein
    dd.Sub_gene.replace(" ", np.nan, inplace=True)
    dd.dropna(subset=["Sub_gene"], inplace=True)

    return dd
#dd.to_csv("checkNoH.csv")


class KinaseSearcher:
    def __init__(self,filename):
        self.filename=filename
        self.open()
        P_cols=["Z_SITE_{}".format(i) for i in range (1,49)]
       # df = df[df[['col_1','col_2']].apply(lambda x: f(*x), axis=1)
        
    def open(self):
        self.data=pd.read_csv(self.filename, header=0)
        
    def findkinase(self,sub_gene, phosphosite):
        a = self.data[self.data.SUB_GENE.str.contains(sub_gene)==True]
        #simple_df['new'] = (simple_df.values == 'AA').any(1).astype(int)
        #print(len(a.index))
        p= (a.values == phosphosite).any(1)
        #print (len(p))
        b=a[p]
        return ",".join(b["KINASE"]) 

def add_kinase(dd, kinase_datafile):
    k=KinaseSearcher(kinase_datafile)    #kinase_substrated_filtered runs up to z_site_48
    #to apply class and populate column for kinase GENE name
    dk=dd.apply(lambda row: k.findkinase(row["Sub_gene"],row["Phosphosite"] ), axis =1)
    dd["Kinase"]= dk

    de = dd.join(dd.pop('Kinase')   #gives multiple-kinase-to-one-sub-gene-phosphosite indv rows
                   .str.strip(',')
                   .str.split(',', expand=True)
                   .stack()
                   .reset_index(level=1, drop=True)
                   .rename('Kinase')).reset_index(drop=True)


    return de



def cv_filter(dd, CV_P):

    dd= dd.loc[(dd['ctrlCV'] <=  CV_P) & (dd['treatCV'] <= CV_P)]   #user define CV value: Rows Above CV_P filtered out
    return dd




def makeplot(df, FC_P, PV_P, Inhibitor):
    

    df.loc[(df['Fold_change'] > FC_P) & (df['p_value'] < PV_P), 'color'] = "green"  # upregulated
    #df.loc - Selects single row or subset of rows from the DataFrame by label
    df.loc[(df['Fold_change'] <=FC_P) & (df['p_value'] < PV_P), 'color'] = "red"   # downregulated
    df['color'].fillna('grey', inplace=True)


    df["log_pvalue"] = -np.log10(df['p_value'])
    df["log_FC"]=np.log2(df['Fold_change'])

    df.head()



    from bokeh.plotting import figure, ColumnDataSource, output_notebook, show
    from bokeh.models import HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool, SaveTool
    from bokeh.palettes import brewer


    output_notebook()


    category = 'Substrate'

    category_items = df[category].unique()

    title = Inhibitor + " : Data Summary"
    #feeding data into ColumnDataSource
    source = ColumnDataSource(df)
    #Editing the hover that need to displayed while hovering
    hover = HoverTool(tooltips=[('Kinase','@Kinase'),
                                ('Substrate', '@Substrate'),
                                ('Sub_gene','@Sub_gene'),
                                ('Phosphosite', '@Phosphosite'),
                               ('Fold_change', '@Fold_change'),
                               ('p_value', '@p_value')])
    #tools that are need to explote data
    tools = [hover, WheelZoomTool(), PanTool(), BoxZoomTool(), ResetTool(), SaveTool()]
    


    #finally making figure with scatter plot
    p = figure(tools=tools,title=title,plot_width=700,plot_height=400,toolbar_location='right',toolbar_sticky=False, )
   
    p.scatter(x='log_FC',y='log_pvalue',source=source,size=10,color='color')
    
    #displaying the graph
    return(p)



def makeplot_2(df, FC_P, PV_P, Inhibitor):


    df = df[df['Kinase']!='']  # user define CV value: Rows Above CV_P filtered out

    df.loc[(df['Fold_change'] > FC_P) & (df['p_value'] < PV_P), 'color' ] = "Blue"  # upregulated
    #df.loc - Selects single row or subset of rows from the DataFrame by label
    df.loc[(df['Fold_change'] <=FC_P) & (df['p_value'] < PV_P), 'color' ] = "Purple"   # downregulated
    df['color'].fillna('grey', inplace=True)
    


    df["log_pvalue"] = -np.log10(df['p_value'])
    df["log_FC"]=np.log2(df['Fold_change'])

    df.head()

    output_notebook()


    category = 'Substrate'

    category_items = df[category].unique()

    title = Inhibitor + " :Data with identified kinases"
    #feeding data into ColumnDataSource
    source = ColumnDataSource(df)
    #Editing the hover that need to displayed while hovering
    hover = HoverTool(tooltips=[('Kinase','@Kinase'),
                                ('Substrate', '@Substrate'),
                                ('Sub_gene','@Sub_gene'),
                                ('Phosphosite', '@Phosphosite'),
                               ('Fold_change', '@Fold_change'),
                               ('p_value', '@p_value')])
    #tools that are need to explote data
    tools = [hover, WheelZoomTool(), PanTool(), BoxZoomTool(), ResetTool(), SaveTool()]
    


    #finally making figure with scatter plot
    p = figure(tools=tools,title=title,plot_width=700,plot_height=400,toolbar_location='right',toolbar_sticky=False, )
   
    p.scatter(x='log_FC',y='log_pvalue',source=source,size=10,color='color')
    
    #displaying the graph
    return(p)



def relative_kinase_activity_calculation(de):

###Sum of control_mean and inhibitor_mean
    #=control mean
    kinase_sum_control_mean= de.groupby("Kinase").Control_mean.sum() #sum of individual group of kinases at a phosphosite
    total_control_mean=de.Control_mean.sum()  #toal sum of control_mean of all kinases

    dkinase=pd.DataFrame(kinase_sum_control_mean)
    dkinase["relative_control_activity"]=dkinase["Control_mean"]/total_control_mean
    #dkinase
    #relative activity = mean of each kinase/total control means
    #-------------
    #inhibitor mean
    kinase_sum_inhibitor_mean= de.groupby("Kinase").Inhibitor_mean.sum() #sum of groups of kinases
    dkinase["Inhibitor_mean"]=kinase_sum_inhibitor_mean
    total_inhibitor_mean=de.Inhibitor_mean.sum()
    dkinase["relative_inhibitor_activity"]=dkinase["Inhibitor_mean"]/total_inhibitor_mean
    #Mean Fold Change
    dkinase["mean_FC_kinase"]= dkinase["Inhibitor_mean"]/dkinase["Control_mean"]
    #----------------
    #dkinase["relative_FC_kinase"]= dkinase["relative_inhibitor_activity"]/dkinase["relative_control_activity"]
    dkinase.sort_values(by='mean_FC_kinase', ascending=False)
    return dkinase.sort_values(by='mean_FC_kinase', ascending=False)#dkinase




def relative_kinase_activity(filename, FC_P, PV_P, CV_P, Inhibitor ):
    input_data=open_file(filename)
    data=filter_data(input_data, FC_P, PV_P, CV_P)
    data=add_sub_gene(data)
    #print(data)
    data=add_kinase(data, "kinase_substrate_filtered.csv")
    #print(data)
    plot1=makeplot(data, FC_P, PV_P, Inhibitor)
    #print(data)
    plot2=makeplot_2(data, FC_P, PV_P, Inhibitor)
    print(data)
    kinase_activity_data=relative_kinase_activity_calculation(data)

    return plot1, plot2, kinase_activity_data
