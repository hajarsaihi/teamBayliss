import pandas as pd

df = pd.read_csv("dataset/kinase_substrate_dataset.csv")     # Reading csv file 
selected = df[(df.KIN_ORGANISM=='human') & (df.SUB_ORGANISM=='human')] # Only data which has the kin_organism and sub_organism as human
selected = selected.drop(columns=['KIN_ORGANISM', 'SUB_ORGANISM', 'DOMAIN', 'IN_VIVO_RXN', 'IN_VITRO_RXN', 'CST_CAT#']) # Drops the columns we don't want
selected = selected.rename(index=str, columns = {'SITE_+/-7_AA': 'SITE_7_AA'}) # Renaming column
selected.to_csv("kinase_substrate.csv", index = False)
print("The kinase_substrate.csv is generated. ")