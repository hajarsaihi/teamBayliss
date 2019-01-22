import pandas as pd

df= pd.read_csv("dataset\phosphorylation_site_dataset.csv")     # Reading csv file 
selected = df[df.ORGANISM == 'human']  # Only data which has the organism as human
selected.to_csv("phosphorylation_site.csv", index = False)
print("The phosphorylation_site.csv is generated. ")