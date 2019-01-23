import pandas
df = pandas.read_csv("raw_inhibitor_data_final.csv", index_col=0)
updated_names = []

for x in df.columns:
    x = x.replace(" ", "_")
    updated_names.append(x)

df.columns = updated_names
df.to_csv("inhibitor_data_final.csv")
