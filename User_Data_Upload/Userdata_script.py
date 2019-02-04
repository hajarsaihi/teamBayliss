
# coding: utf-8

# In[11]:



import pandas as pd
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

d=open_file("az20_500.tsv")



# In[12]:


d_cols=["Substrate", "Control_mean", "Inhibitor_mean", "Fold_change", "p_value", "ctrlCV", "treatCV" ]
d.columns=d_cols

d.head()


# In[13]:


####drop out methonine and none####

import re



d=(d[~d.Substrate.str.contains("None")] ) #drop rows with "None"

patternDel = r"\([M]\d+\)" #Use Regex to find "(M and any number of digits)" #\d+ : one or more digits)

dd=(d[~d.Substrate.str.contains(patternDel)].copy()) #d1: rows with (Mddd) removed....copy() to remove conflict

print(dd.head(30))


# In[14]:


#add split of gene/protein names to XXX_HUMAN   and (SNNN)

dd[["Substrate","Phosphosite"]] = dd.Substrate.str.extract(r"(.+)\((.\d+)", expand=True)
#
print (dd.head(30))


# In[15]:



#https://www.uniprot.org/uniprot/?query=DPOLZ_HUMAN&fil=reviewed%3Ayes&columns=genes(PREFERRED)&format=tab
#https://www.uniprot.org/uniprot/?query=DUS27_HUMAN&columns=genes(PREFERRED)&format=tab
import re
import requests

#Function: Substrates with "_HUMAN" converted to Uniprot Gene Names
def process_query(query):
    
    if re.match(r".+_HUMAN", query):
        URL = 'http://www.uniprot.org/uniprot/?query=' + query + '&columns=genes(PREFERRED)&format=tab'
        r = requests.get(URL)
        lines = r.text.split("\n")
        gene_name=lines[1:2]        #return top preferred uniprot gene result #get accession number
        
        return str(gene_name)  #return gene as string instead of string within a list [""] #get accession number
    else:
        return query
    
process_query("ADT1_HUMAN") #Test
    


# In[16]:


#make copy of Substrate to Substrate gene

dd["Sub_gene"]=dd["Substrate"].copy()


# In[17]:


#Substrates with "_HUMAN" converted to Uniprot Gene Names

dd.Sub_gene = dd.apply(lambda row: process_query(row["Substrate"]), axis =1)

dd["Sub_gene"] = dd["Sub_gene"].str.strip("[]").str.strip("''")  #remove square bracket and '' 
  #remove square bracket and '' 

print(dd.head(5)) #Test


# In[9]:


# 
# dd.to_csv("checkH.csv")


# In[18]:


#Removes Substrates "_HUMAN" with no Sub_gene result: likely experimental protein
dd.Sub_gene.replace(" ", np.nan, inplace=True)
dd.dropna(subset=["Sub_gene"], inplace=True)
#dd.to_csv("checkNoH.csv")


# In[26]:


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
            return ",".join(b["KINASE"]) 
        
        #just the kinase, if not it will return all columns from kinase_substrate
    #and self.data.SUB_MOD_RSD.str.contains(sub_mod_rsd)]
        
k=KinaseSearcher("kinase_substrate.csv")    
k.findkinase("AKT1", "S129")     #Run Test: AKT1(S129)


# In[59]:


# class KinaseSearcher:
#     def __init__(self,filename):
#         self.filename=filename
#         self.open()
        
#     def open(self):
#         self.data=pd.read_csv(self.filename, header=0)
        
#     def findkinase(self,sub_gene, phosphosite):
#         a = self.data[self.data.SUB_GENE.str.contains(sub_gene)==True]
#         #return a
#         #b = a["Z_SITE_{}".format(i)].str.contains(phosphosite)
#         for i in range(1,49,1):
#             b = a[a["Z_SITE_{}".format(i)].str.contains(phosphosite)==True]
#             return b
#             if len(b)== 0:
#                 return None
#             else:
#                 b==phosphosite
#                 return a["KINASE"]
#                 #return b["KINASE"]
        
#         #just the kinase, if not it will return all columns from kinase_substrate
#         #and self.data.SUB_MOD_RSD.str.contains(sub_mod_rsd)]
        
# k=KinaseSearcher("kinase_substrate_filtered.csv")    #kinase_substrated_filtered runs up to z_site_48
# k.findkinase("NCF1", "S303")     #Run Test: AKT1(S129)


# In[27]:


#to apply class and populate column for kinase GENE name
dk=dd.apply(lambda row: k.findkinase(row["Sub_gene"],row["Phosphosite"] ), axis =1)

#dk[14] #Test
#Use Kinase column (not Gene) from kinase_substrate.csv == Name in Kinase_df.csv.


# In[32]:


dd["Kinase"]= dk
dd.head(50)
#dd.to_csv("kinasetosplit.csv")


# In[34]:


# split multiple kinases to one substrate/phosphosite into individual rows
dd = dd.join(dd.pop('Kinase')
                   .str.strip(',')
                   .str.split(',', expand=True)
                   .stack()
                   .reset_index(level=1, drop=True)
                   .rename('Kinase')).reset_index(drop=True)



# In[35]:


def cv_filter(dd, CV_P):

    dd= dd.loc[(dd['ctrlCV'] <=  CV_P) & (dd['treatCV'] <= CV_P)]   #user define CV value: Rows Above CV_P filtered out 
    return dd

cv_filter(dd, 1.0)
#dd.to_csv("check.csv")


# In[78]:



def makeplot(df, FC_P, PV_P, Inhibitor):
    

    df.loc[(df['Fold_change'] > FC_P) & (df['p_value'] < PV_P), 'color'] = "green"  # upregulated
    #df.loc - Selects single row or subset of rows from the DataFrame by label
    df.loc[(df['Fold_change'] <=FC_P) & (df['p_value'] < PV_P), 'color'] = "red"   # downregulated
    df['color'].fillna('grey', inplace=True)


    df["log_pvalue"] = -np.log10(df['p_value'])
    df["log_FC"]=np.log2(df['Fold_change'])

    df.head()




    from bokeh.resources import CDN
    from bokeh.embed import file_html, components
    from bokeh.plotting import figure, ColumnDataSource, output_notebook, show, output_file
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
   
    ##---------displaying the graph
    
    show(p)
    components(p)                    #To get the bokeh html and jazavascript
    script1, div1 =components(p)
    print(script1)    

#makeplot(dd, 1.0, 0.05, "AZ20")

output_file("volcano_plot1.html")  #to output the volcano plot as a html 


makeplot(dd, 1.0, 0.05, "AZ20")

###To get he java script of the Bokeh volcano plot, to ensure the link is dynamic and changes with the newer version of Bokeh that's why these are added here  
 #CDN: Content Delivery Network 
    
cdn_js=CDN.js_files[0]   #Only the first link is used 

#To get the CSS style sheet of the Bokeh volcano plot
cdn_css=CDN.css_files[0] #Only the first link is used 

# In[36]:



#df_vals = df_vals[~df_vals['education'].isnull()] 
dd=dd[~dd["Kinase"].isnull()]  #user define CV value: Rows Above CV_P filtered out 

dd
#dd.to_csv("nonankinase.csv")


# In[77]:



def makeplot_2(df, FC_P, PV_P, Inhibitor):
    
   

    df.loc[(df['Fold_change'] > FC_P) & (df['p_value'] < PV_P), 'color' ] = "Blue"  # upregulated
    #df.loc - Selects single row or subset of rows from the DataFrame by label
    df.loc[(df['Fold_change'] <=FC_P) & (df['p_value'] < PV_P), 'color' ] = "Purple"   # downregulated
    df['color'].fillna('grey', inplace=True)
    


    df["log_pvalue"] = -np.log10(df['p_value'])
    df["log_FC"]=np.log2(df['Fold_change'])

    df.head()


    from bokeh.resources import CDN
    from bokeh.embed import file_html, components
    from bokeh.plotting import figure, ColumnDataSource, output_notebook, show, output_file
    from bokeh.models import HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool, SaveTool
    from bokeh.palettes import brewer

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
    
##---------displaying the graph
    
    show(p)
    components(p)                    #To get the bokeh html and jazavascript
    script1, div1 =components(p)
    print(script1)    

#makeplot(dd, 1.0, 0.05, "AZ20")

output_file("volcano_plot1.html")  #to output the volcano plot as a html 


    
makeplot_2(dd, 1.0, 0.05, "AZ20")

###To get he java script of the Bokeh volcano plot, to ensure the link is dynamic and changes with the newer version of Bokeh that's why these are added here  
 #CDN: Content Delivery Network 
    
cdn_js=CDN.js_files[0]   #Only the first link is used 

#To get the CSS style sheet of the Bokeh volcano plot
cdn_css=CDN.css_files[0] #Only the first link is used 

# In[31]:


##########


# In[37]:


###Sum of control_mean and inhibitor_mean 

#=control mean
kinase_sum_control_mean= dd.groupby("Kinase").Control_mean.sum() #sum of individual group of kinases at a phosphosite
total_control_mean=dd.Control_mean.sum()  #toal sum of control_mean of all kinases

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

#Mean Fold Change
dkinase["mean_FC_kinase"]= dkinase["Inhibitor_mean"]/dkinase["Control_mean"]
#----------------

#dkinase["relative_FC_kinase"]= dkinase["relative_inhibitor_activity"]/dkinase["relative_control_activity"]
dkinase




# In[40]:


dkinase.sort_values(by='mean_FC_kinase', ascending=False)


# In[23]:


#dkinase.to_html('output.html')

