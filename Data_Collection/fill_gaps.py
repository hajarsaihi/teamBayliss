import pandas
df = pandas.read_csv("raw_inhibitor_data_final.csv", index_col=False)

for x in df.columns:
    replace(" ", "_")
    print (x)
