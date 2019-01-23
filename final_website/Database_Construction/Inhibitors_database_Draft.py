import csv, sqlite3


# Create a database in RAM
con = sqlite3.connect('INHIBITOR_KINASE_DATABASE_DRAFT_1.db')


#A cursor object is required to pinpoint data in the database
cur = con.cursor()  

print("Opened database successfully")


#######1: THE INHIBITOR INFORMATION##########

#A table is created

cur.execute("CREATE TABLE inhibitor_information(ChEMBL_ID PRIMARY KEY, INCHI VARCHAR(300), SMILES VARCHAR(30), Name VARCHAR(300), Synonyms VARCHAR(30), Type VARCHAR(30), Max_Phase REAL, Molecular_Weight REAL, Bioactivities REAL, AlogP REAL, PSA REAL, HBA REAL, HBD REAL, RO5_Violations REAL, Rotatable_Bonds REAL, Passes_Ro3 VARCHAR(30), QED_Weighted REAL, ACD_ApKa VARCHAR(50), ACD_BpKa REAL, ACD_LogP REAL, ACD_LogD REAL, Aromatic_Rings VARCHAR(50), Structure_Type VARCHAR(50), Inorganic_Flag REAL, Heavy_Atoms REAL, HBA_Lipinski REAL,HBD_Lipinski REAL, RO5_Violation_Lipinski REAL, Molecular_Weight_Monoisotopic REAL, Molecular_Formula VARCHAR(50), image_link VARCHAR(300));")
 
#The csv file is opened
with open('raw_inhibitor_data_final.csv','rb') as fin: # `with` statement available in 2.5+
	#csv.DictReader uses first line in file for column headings by default
	dr_in_1 = csv.DictReader(fin) # comma is default delimiter
	to_in_1 = [(i['ChEMBL_ID'], i['INCHI'], i['SMILES'], i['Name'], i['Synonyms'], i['Type'], i['Max_Phase'], i['Molecular_Weight'], i['Bioactivities'], i['AlogP'], i['PSA'], i['HBA'], i['HBD'],i['RO5_Violations'], i['Rotatable_Bonds'], i['Passes_Ro3'], i['QED_Weighted'], i['ACD_ApKa'], i['ACD_BpKa'], i['ACD_LogP'], i['ACD_LogD'], i['Aromatic_Rings'], i['Structure_Type'], i['Inorganic_Flag'],i['Heavy_Atoms'], i['HBA_Lipinski'], i['HBD_Lipinski'], i['RO5_Violation_Lipinski'], i['Molecular_Weight_Monoisotopic'], i['Molecular_Formula'], i['image_link'],) for i in dr_in_1]       #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO inhibitor_information(ChEMBL_ID,INCHI,SMILES,Name,Synonyms,Type,Max_Phase,Molecular_Weight,Bioactivities,AlogP,PSA,HBA,HBD,RO5_Violations,Rotatable_Bonds,Passes_Ro3,QED_Weighted,ACD_ApKa,ACD_BpKa,ACD_LogP,ACD_LogD,Aromatic_Rings,Structure_Type,Inorganic_Flag,Heavy_Atoms,HBA_Lipinski,HBD_Lipinski,RO5_Violation_Lipinski,Molecular_Weight_Monoisotopic,Molecular_Formula,image_link) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_in_1)
con.commit()  #Commit the changes 

print to_in_1




#######2: THE INHIBITOR REFERENCES#########

#A table is created

cur.execute("CREATE TABLE inhibitor_references(Key PRIMARY KEY, ChEMBL_ID_, TARGETS, REFERENCE VARCHAR(200), PUBMED_ID VARCHAR(30))") # use your column names here

#The csv file is opened
with open('inhib_and_ref.csv','rb') as fin: # `with` statement available in 2.5+
	#csv.DictReader uses first line in file for column headings by default
    dr_in_2 = csv.DictReader(fin) # comma is default delimiter
    to_in_2 = [(i['Key'],i['ChEMBL_ID_'], i['TARGETS'], i['REFERENCE'], i['PUBMED_ID'],) for i in dr_in_2]    #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO inhibitor_references(Key,ChEMBL_ID_,TARGETS,REFERENCE, PUBMED_ID) VALUES (?,?,?,?,?);", to_in_2)
con.commit()  #Commit the changes 

print to_in_2



### 3: TO JOIN THE TABLES USING A FOREIGN KEY

cur.execute("SELECT ChEMBL_ID FROM inhibitor_information INNER JOIN inhibitor_references ON inhibitor_references.ChEMBL_ID_ = inhibitor_information.ChEMBL_ID ;") 

print(cur.fetchall())

con.commit()


##THE CONNECTION MUST BE CLOSED AT THE END

con.close()