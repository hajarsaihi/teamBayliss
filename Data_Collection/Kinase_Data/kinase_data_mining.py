import pandas
import re

kinase_df = pandas.read_csv("kinase_data.csv")
entrez_df = pandas.read_excel('entrez_to_uniprot.xlsx')

entrez_gene_list = kinase_df['Entrez_GeneID'].values
entrez_ID = entrez_df['entrez_ID'].values

uniprot_IDs = []

for kinase in entrez_gene_list:
    if kinase in entrez_ID:
        ID = entrez_df.loc[entrez_df['entrez_ID'] == kinase,'Entry_name'].iloc[0]
        uniprot_IDs.append(ID)
    else:
        ID = 'unknown'
        uniprot_IDs.append(ID)

kinase_df['uniprot_IDs'] = uniprot_IDs

kinase_list = kinase_df['uniprot_IDs'].values
location_list = []

for kinase in kinase_list:
    kinase = str(kinase)

    if kinase != 'unknown':
        loc = ''
        data = pandas.read_csv("http://www.uniprot.org/uniprot/?query="+kinase+"&sort=score&columns=id,comment(SUBCELLULAR%20LOCATION)&format=tab", sep="\t")
        location = data["Subcellular location [CC]"][0]

        if isinstance(location, str):
            location = location.split('Note')[0]
            location = location.replace('SUBCELLULAR LOCATION: ', '')
            location = location.split(".")

            for x in location:
                if x != ' ':
                    l_final = re.sub(' {.*}', '', x)
                    loc = loc + l_final + "."
            location_list.append(loc)
        else:
            loc = '-'
            location_list.append(loc)
    else:
        loc = '-'
        location_list.append(loc)
kinase_df['location'] = location_list

# Merge alias names for each kinase
alias_names = pandas.read_csv("kinase_alias_names.csv")
name = kinase_df['Name'].values
genes = alias_names['Gene'].values
alias_list = []

for value in name:
    if value in genes:
        final = alias_names.loc[alias_names['Gene'] == value,'Alias'].iloc[0]
        alias_list.append(final)
    else:
        final = value
        alias_list.append(final)

kinase_df['Alias'] = alias_list
kinase_df.to_csv('kinase_df.csv')

################################# Update - need to mine more data from uniprot

# get the accession IDs
import pandas
df = pandas.read_csv("kinase_df.csv", index_col=0)
df = df[df.uniprot_IDs != "unknown"]

uniprot_ID = list(df["uniprot_IDs"])

# just to check :)
# for kinase in uniprot_ID:
 #   if kinase == 'unknown':
  #      print kinase
accID_list = []

for kinase in uniprot_ID:
    data = pandas.read_csv("http://www.uniprot.org/uniprot/?query="+kinase+"&sort=score&columns=id,comment(id)&format=tab", sep="\t")
    accID = data["Entry"][0]
    accID_list.append(accID)
df["uni_accession"] = accID_list

# get gene names
uniprot_ID = list(df["uniprot_IDs"])
gene_name_list = []

for kinase in uniprot_ID:
    data = pandas.read_csv("http://www.uniprot.org/uniprot/?query="+kinase+"&sort=score&columns=id,genes(PREFERRED)&format=tab", sep="\t")
    gene = data["Gene names  (primary )"][0]
    gene_name_list.append(gene)
    
df["gene_name"] = gene_name_list

df=df.drop(columns=['Kinase Domain']) # realised we dont really need this
df.to_csv("kinase_df.csv")
