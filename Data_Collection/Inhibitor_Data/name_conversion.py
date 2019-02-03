import pandas

# Import the data.
df = pandas.read_csv("raw_inhibitor_data_final.csv", index_col=0)
df=df.join(df['TARGETS'].str.split('/', 1, expand=True).rename(columns={0:'TARGETS_1', 1:'TARGETS_2'}))
df=df.drop(columns=['TARGETS'])
df=df.join(df['TARGET_CHEMBL_IDS'].str.split('/', 1, expand=True).rename(columns={0:'Target_ChEMBL_1', 1:'Target_ChEMBL_2'}))
df=df.drop(columns=['TARGET_CHEMBL_IDS'])

# at this point I search the target_chemble_1 on uniprot to get the uniprot identifiers, I get the chembl_uniprot_conv file.
# Then read in this file to get the uniprot names for each of the chemble entries.

chembl_list = list(df['Target_ChEMBL_1'])

conv_df = pandas.read_csv("chembl_uniprot_conv.csv", index_col=1)
conv_chembl = list(conv_df['chembl_id'])
uniprot_list = []

for ID in chembl_list:
    if ID in conv_chembl:
        uniprot_ID = conv_df.loc[conv_df['chembl_id'] == ID,'Entry_name'].iloc[0]
        uniprot_list.append(uniprot_ID)

df["Uniprot_names_1"]= uniprot_list # append list to df

# now for target chemble 2!
# at this point i search the target_chemble_2 on uniprot to get the uniprot identifiers, i get the chembl_uniprot_conv2 file.
chembl_list2 = list(df['Target_ChEMBL_2'])
conv_df2 = pandas.read_csv("chembl_uniprot_conv2.csv", index_col=1)
conv_chembl2 = list(conv_df2['chembl_id'])
uniprot_list2 = []

for ID in chembl_list2:
    if ID in conv_chembl2:
        uniprot_ID = conv_df2.loc[conv_df2['chembl_id'] == ID,'Entry_name'].iloc[0]
        uniprot_list2.append(uniprot_ID)
    else:
        uniprot_ID = " "
        uniprot_list2.append(uniprot_ID)

df["Uniprot_names_2"]= uniprot_list2

#####
# need to then convert the uniprot IDs to the protein names we have in our database (kinase_df)!
kinase_df = pandas.read_csv("kinase_df.csv", index_col=0)
uni_ID_list = list (kinase_df["uniprot_IDs"])
final_names = []

for name in uniprot_list: #first set of targets first!
    if name in uni_ID_list:
        prot_name = kinase_df.loc[kinase_df['uniprot_IDs'] == name,'Name'].iloc[0]
        final_names.append(prot_name)

df["TARGETS_1"]= final_names

final_names2 = []

for name in uniprot_list2: #second set of targets!
    if (name in uni_ID_list) and (name!=" "): #make sure there is no gaps
        prot_name = kinase_df.loc[kinase_df['uniprot_IDs'] == name,'Name'].iloc[0]
        final_names2.append(prot_name)
    else:
        prot_name = " "
        final_names2.append(prot_name)

df["TARGETS_2"]= final_names2

df=df.drop(columns=["Target_ChEMBL_1","Target_ChEMBL_2","Uniprot_names_1","Uniprot_names_2"]) #dont need these anymore
df.to_csv('raw_inhibitor_data_final.csv')
