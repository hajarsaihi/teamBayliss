# Convert the kinase name to the uniprot iDs in order to get the location from uniprot. 
import pandas

kinase_df = pandas.read_csv("kinase_data.csv")
uniprot_df = pandas.read_excel('uniprot_identifiers.xlsx')

name = kinase_df['Name'].values
uniprot_name = uniprot_df['Gene'].values

uniprot_IDs = []


for kinase in name:
    if kinase in uniprot_name:
        ID = uniprot_df.loc[uniprot_df['Gene'] == kinase,'Uniprot_id'].iloc[0]
        uniprot_IDs.append(ID)
    else:
        ID = 'none'
        uniprot_IDs.append(ID)

kinase_df['uniprot_IDs'] = uniprot_IDs
kinase_list = kinase_df['uniprot_IDs'].values
location_list = []

for kinase in kinase_list:
    kinase = str(kinase)
    
    if kinase != 'none':
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
            loc = 'location unknown'
            location_list.append(loc)
    else:
        loc = 'location unknown'
        location_list.append(loc)
        
kinase_df['location'] = location_list
kinase_df.to_csv('kinase_df.csv')
