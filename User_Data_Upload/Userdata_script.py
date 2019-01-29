
# coding: utf-8

# In[34]:



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


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

d=open_file("az20.tsv")



# In[35]:


d_cols=["Substrate", "Control_mean", "Inhibitor_mean", "Fold_change", "p_value", "ctrlCV", "treatCV" ]
d.columns=d_cols

d.head(30)


# In[36]:


####drop out methonine and none####

import re


d=(d[~d.Substrate.str.contains("None")] ) #drop rows with "None"

patternDel = r"\([M]\d+\)" #Use Regex to find "(M and any number of digits)" #\d+ : one or more digits)

dd=(d[~d.Substrate.str.contains(patternDel)].copy()) #d1: rows with (Mddd) removed....copy() to remove conflict

print(dd.head(30))


# In[39]:


#add split of gene/protein names to XXX_HUMAN   and (SNNN)

dd[["Substrate","Phosphosite"]] = dd.Substrate.str.extract(r"(.+)\((.\d+)", expand=True)
#
print (dd.head(30))


# In[90]:



#https://www.uniprot.org/uniprot/?query=DPOLZ_HUMAN&fil=reviewed%3Ayes&columns=genes(PREFERRED)&format=tab
#https://www.uniprot.org/uniprot/?query=DUS27_HUMAN&columns=genes(PREFERRED)&format=tab
import re
import requests

def process_query(query):
    
    if re.match(r".+_HUMAN", query):
        URL = 'http://www.uniprot.org/uniprot/?query=' + query + '&columns=genes(PREFERRED)&format=tab'
        r = requests.get(URL)
        lines = r.text.split("\n")
        gene_name=lines[1:2]        #return top preferred uniprot gene result
        
        return str(gene_name)  #return gene as string instead of string within a list [""]
    else:
        return query
    
#process_query("ADT1_HUMAN") #Test
    


# In[91]:


#make copy of Substrate to Substrate gene

dd["Sub_gene"]=dd["Substrate"].copy()


# In[92]:



dd.Sub_gene = dd.apply(lambda row: process_query(row["Substrate"]), axis =1)

dd["Sub_gene"] = dd["Sub_gene"].str.strip("[]").str.strip("''")  #remove square bracket and '' 

#print(dd.head(5)) #Test


# In[48]:


#make Kinase column, match Gene to Phosphosite to Kinase info from Kinase_substrate.csv
class KinaseSearcher:
    def __init__(self,filename):
        self.filename=filename
        self.open()
        
    def open(self):
        self.data=pd.read_csv(self.filename, header=0)
        
    def findkinase(self,sub_gene, sub_mod_rsd):
        a = self.data[self.data.SUB_GENE.str.contains(sub_gene)==True]
        b = a[a.SUB_MOD_RSD.str.contains(sub_mod_rsd)==True]
        if len(b.index)== 0:
            return None
        else:
            return ",".join(b["KINASE"]) #just the kinase
    #and self.data.SUB_MOD_RSD.str.contains(sub_mod_rsd)]
        
k=KinaseSearcher("kinase_substrate.csv")    
#k.findkinase("AKT1", "S129")     #Run Test: AKT1(S129)


# In[49]:


#to apply class and populate column for kinase GENE name
dk=dd.apply(lambda row: k.findkinase(row["Sub_gene"],row["Phosphosite"] ), axis =1)

#dk[14] #Test
#Use Kinase column (not Gene) from kinase_substrate.csv == Name in Kinase_df.csv.


# In[51]:


dd["Kinase"]= dk
#dd


# In[88]:


def cv_filter(dd, CV_P):

    dd= dd.loc[(dd['ctrlCV'] <=  CV_P) & (dd['treatCV'] <= CV_P)]   #user define CV value: Rows Above CV_P filtered out 
    return dd

cv_filter(dd, 1.0)


# In[89]:



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

    title = Inhibitor
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
    show(p)
    
makeplot(dd, 1.0, 0.05, "AZ20")


# In[ ]:


##########


# In[63]:


###Sum of control_mean and inhibitor_mean 

#=control mean
kinase_sum_control_mean= dd.groupby("Kinase").Control_mean.sum() #sum of groups of kinases
total_control_mean=dd.Control_mean.sum()

dkinase=pd.DataFrame(kinase_sum_control_mean)
dkinase["relative_control_activity"]=dkinase["Control_mean"]/total_control_mean
#dkinase
#relative activity = mean of each kinase/total control means


#-------------
#inhibitor mean
kinase_sum_inhibitor_mean= dd.groupby("Kinase").Inhibitor_mean.sum() #sum of groups of kinases
dkinase["Inhibitor_mean"]=kinase_sum_inhibitor_mean
total_inhibitor_mean=dd.Inhibitor_mean.sum()
dkinase["relative_inhibitor_activity"]=dkinase["Inhibitor_mean"]/total_inhibitor_mean
#total_control_mean=dd.Control_mean.sum()
dkinase



# In[ ]:


df.sort_values(by='AZ20_p-value', ascending=True)


# In[ ]:


#Print top 30 p-values

df.sort_values(by='AZ20_p-value', ascending=True).head(30)


# In[ ]:


#export top 30 results to a database
#Sqllit

import sqlite3

conn = sqlite3.connect("AZ20_upload.db") #creates the database if it does not exist

cur = conn.cursor()

cur.execute("CREATE TABLE top_results (Substrate TEXT, pvalue FLOAT)")





# In[ ]:


df_filtered = df.sort_values(by='AZ20_p-value', ascending=True).head(30)


df_filtered.to_sql("Substrate", conn, if_exists="replace")


pd.read_sql_query("select * from top_results;", conn)

