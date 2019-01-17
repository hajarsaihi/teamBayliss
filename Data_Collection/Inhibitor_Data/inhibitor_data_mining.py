# Data Mining inhibitor data!
# Import the tools needed.
import pandas

# Import the data.
comp_data = pandas.read_csv("raw_inhibitor_data.csv", index_col=False)
comp_specifics = pandas.read_csv("comp_specifics.csv")

# The ChEMBL_ID name doesnt match on the two databases so needs to be changed.
comp_data = comp_data.rename(index=str, columns={"CHEMBL_ID": "ChEMBL_ID"})

# Define a new compounds list.
compounds = list(comp_data.ChEMBL_ID)

# Subset the data and extract the rows where the ChEMBL_ID matches that from the
# compounds list.
comp_specifics = comp_specifics[comp_specifics['ChEMBL_ID'].isin(compounds)]

# Define another compounds list from the compound specifics database.
compounds2 = list(comp_specifics.ChEMBL_ID)

# Subset the data - check if there are any compounds from the raw inhibitor data
# that aren't in the compound specifics data set.
comp_data = comp_data[comp_data['ChEMBL_ID'].isin(compounds2)]

# Make the inhibitor_references table.
inhibitor_references = comp_data.drop(columns=['GSK_REG_NO', 'MOLREGNO',
                                                'INCHI','SMILES', 'PARENT_CHEMBL_ID',
                                                'PARENT_INCHI','PARENT_SMILES','TARGETS',
                                                'TARGET_CHEMBL_IDS','REF_CHEMBL_ID'], axis=1)

inhibitor_references.to_csv('inhibitor_references.csv')

# Merge comp_specifics and comp_data into one table based on the ID.
comp_data = comp_data.join(comp_specifics.set_index('ChEMBL_ID'), on='ChEMBL_ID')

# Drop the columns that arent needed.
comp_data = comp_data.drop(columns=['PARENT_CHEMBL_ID', 'PARENT_INCHI',
                                    'PARENT_SMILES','TARGETS', 'TARGET_CHEMBL_IDS',
                                    'REF_CHEMBL_ID','REFERENCE','PUBMED_ID',
                                    'GSK_REG_NO','MOLREGNO','Molecular Species','Targets'], axis=1)

# Output to final CSV.
comp_data.to_csv('raw_inhibitor_data_final.csv')
