import pandas as pd

df = pd.read_csv("dataset\kinase_substrate_dataset.csv")     # Reading csv file 
selected = df[(df.KIN_ORGANISM=='human') & (df.SUB_ORGANISM=='human')] # Only data which has the kin_organism and sub_organism as human
selected.drop(columns=['KIN_ORGANISM', 'SUB_ORGANISM'])
selected.to_csv("kinase_substrate.csv", index = False)
print("The kinase_substrate.csv is generated. ")