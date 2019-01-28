import csv, sqlite3


# Create a database in RAM
con = sqlite3.connect('FULL_DATABASE_DRAFT_3.db')


#A cursor object is required to pinpoint data in the database
cur = con.cursor()  

print("Opened database successfully")

###############################~~~~~~~~~~~~~~~~INHIBITORS TABLES~~~~~~~~~~~~##################################

#######1: THE INHIBITOR INFORMATION ##########

#A table is created

cur.execute("CREATE TABLE inhibitor_information(ChEMBL_IDs PRIMARY KEY, INCHI VARCHAR(300), SMILES VARCHAR(30),TARGETS_1 TEXT, TARGETS_2 TEXT,Name VARCHAR(300),\
												 Synonyms VARCHAR(30), Type VARCHAR(30), Max_Phase REAL, Molecular_Weight REAL, Bioactivities REAL,\
												 AlogP REAL, PSA REAL, HBA REAL, HBD REAL, RO5_Violations REAL, Rotatable_Bonds REAL,\
												 Passes_Ro3 VARCHAR(30), QED_Weighted REAL, ACD_ApKa VARCHAR(50), ACD_BpKa REAL,\
												 ACD_LogP REAL, ACD_LogD REAL, Aromatic_Rings VARCHAR(50), Structure_Type VARCHAR(50),\
												Inorganic_Flag REAL, Heavy_Atoms REAL, HBA_Lipinski REAL,HBD_Lipinski REAL, RO5_Violations_Lipinski REAL,\
												 Molecular_Weight_Monoisotopic REAL, Molecular_Formula VARCHAR(50), image_link VARCHAR(300));")
 
#The csv file is opened
with open('raw_inhibitor_data_final.csv','rb') as fin: # reads file in Binary mode, fin is the file name which is used below 
	#csv.DictReader uses first line in file for column headings by default
	dr_in_1 = csv.DictReader(fin) # comma is default delimiter, Each row read from the csv file is returned as a list of strings
	to_in_1 = [(i['ChEMBL_IDs'], i['INCHI'], i['SMILES'], i['TARGETS_1'], i['TARGETS_2'],i['Name'],i['Synonyms'], i['Type'], i['Max_Phase'], i['Molecular_Weight'],\
		       i['Bioactivities'], i['AlogP'], i['PSA'], i['HBA'], i['HBD'],i['RO5_Violations'], i['Rotatable_Bonds'], i['Passes_Ro3'],\
		       i['QED_Weighted'], i['ACD_ApKa'], i['ACD_BpKa'], i['ACD_LogP'], i['ACD_LogD'], i['Aromatic_Rings'], i['Structure_Type'],\
		       i['Inorganic_Flag'],i['Heavy_Atoms'], i['HBA_Lipinski'], i['HBD_Lipinski'], i['RO5_Violations_Lipinski'],\
		       i['Molecular_Weight_Monoisotopic'], i['Molecular_Formula'], i['image_link'],) for i in dr_in_1]       #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO inhibitor_information(ChEMBL_IDs, INCHI,SMILES,TARGETS_1, TARGETS_2, Name,Synonyms,Type,Max_Phase,\
	Molecular_Weight,Bioactivities,AlogP,PSA,HBA,HBD,RO5_Violations,Rotatable_Bonds,Passes_Ro3,QED_Weighted,\
	ACD_ApKa,ACD_BpKa,ACD_LogP,ACD_LogD,Aromatic_Rings,Structure_Type,Inorganic_Flag,Heavy_Atoms,HBA_Lipinski,\
	HBD_Lipinski,RO5_Violations_Lipinski,Molecular_Weight_Monoisotopic,Molecular_Formula,image_link)\
	VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_in_1)
con.commit()  #Commit the changes 

#print to_in_1




#######2: THE INHIBITOR REFERENCES #########

#A table is created

cur.execute("CREATE TABLE inhibitor_references(Key PRIMARY KEY, ChEMBL_ID_, TARGET_1,TARGET_2, PUBMED_ID VARCHAR(30))") # use your column names here

#The csv file is opened
with open('inhib_and_ref.csv','rb') as fin: # `with` statement available in 2.5+
	#csv.DictReader uses first line in file for column headings by default
    dr_in_2 = csv.DictReader(fin) # comma is default delimiter
    to_in_2 = [(i['Key'],i['ChEMBL_ID_'], i['TARGET_1'], i['TARGET_2'],i['PUBMED_ID'],) for i in dr_in_2]    #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO inhibitor_references(Key,ChEMBL_ID_,TARGET_1, TARGET_2, PUBMED_ID) VALUES (?,?,?,?,?);", to_in_2)
con.commit()  #Commit the changes 

#print to_in_2




#######3: THE INHIBITOR-KINASE TABLE #########

#A table is created

cur.execute("CREATE TABLE inhibitor_KINASE(Primary_Key PRIMARY KEY, ChEMBL_ID TEXT,TARGETs_1 TEXT, TARGETs_2 TEXT);")
 
#The csv file is opened
with open('raw_inhibitor_data_final.csv','rb') as fin: # reads file in Binary mode, fin is the file name which is used below 
	#csv.DictReader uses first line in file for column headings by default
	dr_in_3 = csv.DictReader(fin) # comma is default delimiter, Each row read from the csv file is returned as a list of strings
	to_in_3 = [(i['Primary_Key'], i['ChEMBL_IDs'], i['TARGETS_1'],i['TARGETS_2'],) for i in dr_in_3]       #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO inhibitor_KINASE(Primary_Key, ChEMBL_ID ,TARGETs_1, TARGETs_2 )\
	VALUES (?,?,?,?);", to_in_3)
con.commit()  #Commit the changes 

#print to_in_3





### 4: TO JOIN THE TABLES USING A FOREIGN KEY ########

cur.execute("SELECT ChEMBL_IDs, ChEMBL_ID_ FROM inhibitor_information, inhibitor_references  INNER JOIN inhibitor_KINASE ON inhibitor_KINASE.ChEMBL_ID = inhibitor_information.ChEMBL_IDs or inhibitor_references.ChEMBL_ID_ ;") 
#print(cur.fetchall())
con.commit()
#cur.execute("SELECT ChEMBL_IDs FROM inhibitor_information  INNER JOIN inhibitor_references ON inhibitor_references.ChEMBL_ID_ = inhibitor_information.ChEMBL_IDs ;") 

cur.execute("SELECT TARGET_1 FROM inhibitor_references INNER JOIN inhibitor_information, inhibitor_KINASE ON inhibitor_references.TARGET_1  = inhibitor_information.TARGETS_1 or inhibitor_KINASE.TARGETs_1;") 
#print(cur.fetchall())
con.commit()

cur.execute("SELECT TARGET_2 FROM inhibitor_references INNER JOIN inhibitor_information, inhibitor_KINASE ON inhibitor_references.TARGET_2  = inhibitor_information.TARGETS_2 or inhibitor_KINASE.TARGETs_2;") 
#print(cur.fetchall())
con.commit()








###############################~~~~~~~~~~~~~~~~KINASE TABLES~~~~~~~~~~~~##################################
#######1: THE KINASE INFORMATION##########

#A table is created

cur.execute("CREATE TABLE Kinase_Information(key_numbers PRIMARY KEY, Name VARCHAR(30), Groups TEXT, Family VARCHAR(30), Subfamily VARCHAR(30),\
                                            Entrez_GeneID VARCHAR(30), Entrez_description REAL,uniprot_IDs TEXT, location TEXT, Alias VARCHAR(200));") # use your column names here

#The csv file is opened
with open('kinase_df.csv','rb') as fin: # reads file in Binary mode, 
    #csv.DictReader uses first line in file for column headings by default
    dr_1 = csv.DictReader(fin) # comma is default delimiter
    to_db_1 = [(i['key_numbers'],i['Name'], i['Groups'],i['Family'], i['Subfamily'], i['Entrez_GeneID'],\
                i['Entrez_description'],i['uniprot_IDs'], i['location'], i['Alias']) for i in dr_1]    #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO Kinase_Information(key_numbers,Name, Groups, Family, Subfamily, Entrez_GeneID,\
                 Entrez_description, uniprot_IDs, location, Alias ) VALUES (?,?,?,?,?,?,?,?,?,?);", to_db_1)
con.commit()  #Commit the changes 

#print to_db_1

#######2: THE KINASE PHOSPHOSITES##########


cur.execute("CREATE TABLE Kinase_Phosphosite(Keys_row PRIMARY KEY, GENE TEXT, KINASE VARCHAR(30), KIN_ACC_ID VARCHAR(30),\
				 SUBSTRATE TEXT, SUB_ACC_ID VARCHAR(30),SUB_GENE VARCHAR(20),SUB_MOD_RSD TEXT,\
				 SITE_GRP_ID INTEGER,SITE_7_AA VARCHAR(16));") # use your column names here

with open('kinase_substrate.csv','rb') as fin: # `with` statement available in 2.5+
   # csv.DictReader uses first line in file for column headings by default
    dr_2 = csv.DictReader(fin) # comma is default delimiter
    to_db_2 = [(i['Keys_row'],i['GENE'], i['KINASE'], i['KIN_ACC_ID'], i['SUBSTRATE'], i['SUB_ACC_ID'], i['SUB_GENE'], \
    			i['SUB_MOD_RSD'], i['SITE_GRP_ID'], i['SITE_7_AA'] ) for i in dr_2]

cur.executemany("INSERT INTO Kinase_Phosphosite(Keys_row,GENE, KINASE, KIN_ACC_ID, SUBSTRATE, SUB_ACC_ID, SUB_GENE,\
				 SUB_MOD_RSD, SITE_GRP_ID, SITE_7_AA) VALUES (?,?,?,?,?,?,?,?,?,?);", to_db_2)

con.commit()

#print to_db_2


### 4: TO JOIN THE TABLES USING A FOREIGN KEY ########

#Joined the Kinase tables

cur.execute("SELECT Name FROM Kinase_Information INNER JOIN Kinase_Phosphosite ON Kinase_Phosphosite.KINASE = Kinase_Information.Name ;") 

#con.commit()

#print(cur.fetchall())


#Joined the Inhibitor and Kinase information tables

cur.execute("SELECT TARGETS_1, TARGETS_2 FROM inhibitor_information INNER JOIN Kinase_Information ON Kinase_Information.Name = inhibitor_information.TARGETS_1 OR inhibitor_information.TARGETS_2  ;") 

#print(cur.fetchall())

con.commit()


##THE CONNECTION MUST BE CLOSED AT THE END

con.close()











