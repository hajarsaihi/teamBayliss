import pandas as pd
import numpy as np
import collections
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("phosphorylation.csv") 
data = open("keep_names.txt","r").read().split("\n")
print("Actual number of rows : ", len(df))

df['PROTEIN'] = list(map(lambda x: x.lower(), df['PROTEIN']))
df = df[df.PROTEIN.isin(data)]

n_df = df[~df.PROTEIN.duplicated()]
print("After removing : ",len(n_df))
n_df.to_csv("Locations.csv",index=False)
print("Done Successfully! ")