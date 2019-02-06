import pandas as pd

df= pd.read_csv("data.csv")     # Reading csv file 
data = open("gene_list.txt").read().split("\n")  # Reading gene list 
selected = df[df.GENE.isin((data))]  # Only data which is the correct gene
selected = selected[selected.ORGANISM=='human']  # Only data which has the organism as human
selected.to_csv("output.csv", index = False)
print("The output.csv is generated. ")