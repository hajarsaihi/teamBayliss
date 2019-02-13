import pandas as pd
import numpy as np
df = pd.read_csv("kinase_substrate_filtered.csv")
df1 = pd.read_csv("phosphorylation_site.csv")
lst = []
dc = {}
c= 0
print(len(df.SUBSTRATE.values))
for i in range(len(df.SUBSTRATE.values)):
    if df.loc[i,"SUBSTRATE"] in df1.PROTEIN.values and df.loc[i,"SUBSTRATE"] not in dc.keys():
        ls = df1[df.loc[i,"SUBSTRATE"]==df1.PROTEIN]["HU_CHR_LOC"].values
        lst.append(ls[0])
    elif df.loc[i,"SUBSTRATE"] not in df1.PROTEIN.values:
        lst.append(" ")
data= lst
column = "HU_CHR_LOC"
df.insert(4,column,data)
df.to_csv("RESULT.csv",index=False)
print("RESULT.csv is generated successfully")