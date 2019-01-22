import csv, sqlite3


# Create a database in RAM
con = sqlite3.connect('final_data.db')


#A cursor object is required to pinpoint data in the database
cur = con.cursor()

print("Opened database successfully")

#######1: THE KINASE INFORMATION##########

#A table is created

cur.execute("CREATE TABLE Kinase_Information(Kinase_Name PRIMARY KEY, Family VARCHAR(30), SubFamily VARCHAR(30), ENTREZ_GENEID VARCHAR(30), Location TEXT);") # use your column names here

#The csv file is opened
with open('KinaseInformation.csv','rb') as fin: # `with` statement available in 2.5+
	#csv.DictReader uses first line in file for column headings by default
    dr_1 = csv.DictReader(fin) # comma is default delimiter
    to_db_1 = [(i['Kinase_Name'], i['Family'], i['SubFamily'], i['ENTREZ_GENEID'], i['Location']) for i in dr_1]    #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO Kinase_Information(Kinase_Name, Family, SubFamily, ENTREZ_GENEID, Location) VALUES (?, ?,?,?,?);", to_db_1)
con.commit()  #Commit the changes

print to_db_1


#######2: THE KINASE PHOSPHOSITES##########

cur.execute("CREATE TABLE Kinase_Phosphosite(Phosphosite_ID PRIMARY KEY, GENE VARCHAR(30), HU_CHR_LOC VARCHAR(30), MOD_RSD VARCHAR(30), ACC_ID VARCHAR(30), SITE_SEQ VARCHAR(20) );") # use your column names here

with open('Kinase_Phosphosite.csv','rb') as fin: # `with` statement available in 2.5+
   # csv.DictReader uses first line in file for column headings by default
    dr_2 = csv.DictReader(fin) # comma is default delimiter
    to_db_2 = [(i['Phosphosite_ID'], i['GENE'], i['HU_CHR_LOC'], i['MOD_RSD'], i['ACC_ID'], i['SITE_SEQ']) for i in dr_2]

cur.executemany("INSERT INTO Kinase_Phosphosite(Phosphosite_ID, GENE, HU_CHR_LOC, MOD_RSD, ACC_ID, SITE_SEQ ) VALUES (?,?,?,?,?,?);", to_db_2)

con.commit()

print to_db_2



#######3: THE INTERACTING KINASE ##########

cur.execute("CREATE TABLE InteractingKinase(Interaction_ID PRIMARY KEY, Action_Kinase VARCHAR(30), Target_Kinase VARCHAR(30), MOD_RSD VARCHAR(30) );") # use your column names here

with open('InteractingKinase.csv','rb') as fin: # `with` statement available in 2.5+
   # csv.DictReader uses first line in file for column headings by default
    dr_3 = csv.DictReader(fin) # comma is default delimiter
    to_db_3 = [(i['Interaction_ID'],i['Action_Kinase'], i['Target_Kinase'], i['MOD_RSD'],) for i in dr_3]

cur.executemany("INSERT INTO InteractingKinase(Interaction_ID, Action_Kinase, Target_Kinase, MOD_RSD) VALUES (?,?,?,?);", to_db_3)

con.commit()

print to_db_3


### 5: TO JOIN THE TABLES USING A FOREIGN KEY

cur.execute("SELECT Kinase_Name FROM Kinase_Information INNER JOIN Kinase_Phosphosite ON Kinase_Phosphosite.GENE = Kinase_Information.Kinase_Name ;")

cur.execute("SELECT Kinase_Name FROM Kinase_Information INNER JOIN InteractingKinase ON InteractingKinase.Target_Kinase = Kinase_Information.Kinase_Name ;")

print(cur.fetchall())

con.commit()


##THE CONNECTION MUST BE CLOSED AT THE END

con.close()
