import csv, sqlite3


# Create a database in RAM
con = sqlite3.connect('final_data.db')


#A cursor object is required to pinpoint data in the database
cur = con.cursor()

print("Opened database successfully")

#######1: THE KINASE INFORMATION##########

#A table is created

cur.execute("CREATE TABLE Kinase_Information(key_numbers, Name  PRIMARY KEY, Groups TEXT, Family VARCHAR(30), Subfamily VARCHAR(30), Entrez_GeneID VARCHAR(30), Entrez_description REAL, location, Alias);") # use your column names here

#The csv file is opened
with open('kinase_df.csv','rb') as fin: # `with` statement available in 2.5+
	#csv.DictReader uses first line in file for column headings by default
    dr_1 = csv.DictReader(fin) # comma is default delimiter
    to_db_1 = [(i['key_numbers'],i['Name'], i['Groups'],i['Family'], i['Subfamily'], i['Entrez_GeneID'],i['Entrez_description'], i['location'], i['Alias']) for i in dr_1]    #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO Kinase_Information(key_numbers,Name, Groups, Family, Subfamily, Entrez_GeneID, Entrez_description,location, Alias) VALUES (?,?,?,?,?,?,?,?,?);", to_db_1)
con.commit()  #Commit the changes

print to_db_1


#######2: THE KINASE PHOSPHOSITES##########

cur.execute("CREATE TABLE Kinase_Phosphosite_1(Phosphosite_ID PRIMARY KEY, GENE VARCHAR(30), HU_CHR_LOC VARCHAR(30), MOD_RSD VARCHAR(30), ACC_ID VARCHAR(30), SITE_SEQ VARCHAR(20) );") # use your column names here

with open('Kinase_Phosphosite.csv','rb') as fin: # `with` statement available in 2.5+
   # csv.DictReader uses first line in file for column headings by default
    dr_2 = csv.DictReader(fin) # comma is default delimiter
    to_db_2 = [(i['Phosphosite_ID'], i['GENE'], i['HU_CHR_LOC'], i['MOD_RSD'], i['ACC_ID'], i['SITE_SEQ']) for i in dr_2]

cur.executemany("INSERT INTO Kinase_Phosphosite_1(Phosphosite_ID, GENE, HU_CHR_LOC, MOD_RSD, ACC_ID, SITE_SEQ ) VALUES (?,?,?,?,?,?);", to_db_2)

con.commit()

print to_db_2



#######3: THE INTERACTING KINASE ##########

cur.execute("CREATE TABLE InteractingKinase_1(Interaction_ID PRIMARY KEY, Action_Kinase VARCHAR(30), Target_Kinase VARCHAR(30), MOD_RSD VARCHAR(30) );") # use your column names here

with open('InteractingKinase.csv','rb') as fin: # `with` statement available in 2.5+
   # csv.DictReader uses first line in file for column headings by default
    dr_3 = csv.DictReader(fin) # comma is default delimiter
    to_db_3 = [(i['Interaction_ID'],i['Action_Kinase'], i['Target_Kinase'], i['MOD_RSD'],) for i in dr_3]

cur.executemany("INSERT INTO InteractingKinase_1(Interaction_ID, Action_Kinase, Target_Kinase, MOD_RSD) VALUES (?,?,?,?);", to_db_3)

con.commit()

print to_db_3


### 5: TO JOIN THE TABLES USING A FOREIGN KEY

cur.execute("SELECT Name FROM Kinase_Information INNER JOIN Kinase_Phosphosite_1 ON Kinase_Phosphosite_1.GENE = Kinase_Information.Name ;")

cur.execute("SELECT Name FROM Kinase_Information INNER JOIN InteractingKinase_1 ON InteractingKinase_1.Target_Kinase = Kinase_Information.Name ;")

print(cur.fetchall())

con.commit()


##THE CONNECTION MUST BE CLOSED AT THE END

con.close()
