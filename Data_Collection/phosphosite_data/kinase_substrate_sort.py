import pandas as pd
import numpy as np
import collections
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("kinase_substrate.csv")
df=df.drop(labels=["SITE_GRP_ID","SITE_7_AA"],axis=1) # drop two columns 
sub_mod= df["SUB_MOD_RSD"].values
kinase =df["KINASE"].values
subs = df["SUBSTRATE"].values
new_df = pd.DataFrame({"KINASE" : kinase,"SUBSTRATE" : subs,"SUB_MOD_RSD" : sub_mod})
col=["GENE","KINASE","KIN_ACC_ID","SUBSTRATE","SUB_GENE_ID","SUB_ACC_ID","SUB_GENE","Z_SITE_1"]
result = pd.DataFrame({"GENE":[],"KINASE":[],"KIN_ACC_ID":[],"SUBSTRATE":[],"SUB_GENE_ID":[],"SUB_ACC_ID":[],"SUB_GENE":[],"Z_SITE_1":[]})
for i in range(len(kinase)):
    count=2
    col=["GENE","KINASE","KIN_ACC_ID","SUBSTRATE","SUB_GENE_ID","SUB_ACC_ID","SUB_GENE","Z_SITE_1"]
    if i in df.index:
        datta = list(df.loc[i,:].values)
    else:
        continue
    dic = collections.defaultdict()
    for k in range(len(col)):
        dic[col[k]]=[datta[k]]
    lst= list(df[(df["KINASE"]==new_df.loc[i,"KINASE"]) & (df["SUBSTRATE"]==new_df.loc[i,"SUBSTRATE"])]["SUB_MOD_RSD"].values)
    if df.loc[i,"SUB_MOD_RSD"]==np.nan:
        continue 
    if df.loc[i,"SUB_MOD_RSD"] in lst:
        lst.remove(df.loc[i,"SUB_MOD_RSD"])
    else:
        continue
    for j in lst:
        dic["Z_SITE_"+str(count)]=[j]
        col.append("Z_SITE_"+str(count))
        count+=1
    datta = np.array(datta)
    datta= datta.reshape((1,datta.shape[0])) 
    n_df = pd.DataFrame(dic)
    result = pd.concat([result,n_df]).fillna(" ")
    df = df.drop(df[(df["KINASE"]==new_df.loc[i,"KINASE"]) & (df["SUBSTRATE"]==new_df.loc[i,"SUBSTRATE"])].index)
def srt(x):
    return int(x[7:])
colm = sorted(result.columns[8:].values,key=srt) # Sort site columns 
colm = list(result.columns[:8].values)+colm 
Rsult= result[colm]
end = len(Rsult)
start = 6000
numbers = [i for i in range(start,start+end,1)]
Rsult.insert(loc=0, column='Key_rows', value=numbers)
Rsult.to_csv("kinase_substrate_filtered.csv",index=False)
print("Done Successfully...! ")