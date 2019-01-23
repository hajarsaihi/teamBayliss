import csv, sqlite3


# Create a database in RAM
con = sqlite3.connect('PROTEIN_KINASE_DATABASE_DRAFT_3.db')


#A cursor object is required to pinpoint data in the database
cur = con.cursor()  

print("Opened database successfully")

#######1: THE KINASE INFORMATION##########

#A table is created

cur.execute("CREATE TABLE Kinase_Information(key_numbers PRIMARY KEY, Name, Groups TEXT, Family VARCHAR(30), Subfamily VARCHAR(30),\
											Entrez_GeneID VARCHAR(30), Entrez_description REAL, location, Alias);") # use your column names here

#The csv file is opened
with open('kinase_df.csv','rb') as fin: # reads file in Binary mode, 
	#csv.DictReader uses first line in file for column headings by default
    dr_1 = csv.DictReader(fin) # comma is default delimiter
    to_db_1 = [(i['key_numbers'],i['Name'], i['Groups'],i['Family'], i['Subfamily'], i['Entrez_GeneID'],\
    			i['Entrez_description'], i['location'], i['Alias']) for i in dr_1]    #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO Kinase_Information(key_numbers,Name, Groups, Family, Subfamily, Entrez_GeneID,\
				 Entrez_description,location, Alias) VALUES (?,?,?,?,?,?,?,?,?);", to_db_1)
con.commit()  #Commit the changes 

print to_db_1


#######2: THE KINASE PHOSPHOSITES##########

cur.execute("CREATE TABLE Kinase_Phosphosite(Keys_ PRIMARY KEY, GENE TEXT, KINASE VARCHAR(30), KIN_ACC_ID VARCHAR(30),\
				 SUBSTRATE TEXT, SUB_ACC_ID VARCHAR(30),SUB_GENE VARCHAR(20),SUB_MOD_RSD TEXT,\
				 SITE_GRP_ID INTEGER,SITE_7_AA VARCHAR(16));") # use your column names here

with open('kinase_substrate.csv','rb') as fin: # `with` statement available in 2.5+
   # csv.DictReader uses first line in file for column headings by default
    dr_2 = csv.DictReader(fin) # comma is default delimiter
    to_db_2 = [(i['Keys_'],i['GENE'], i['KINASE'], i['KIN_ACC_ID'], i['SUBSTRATE'], i['SUB_ACC_ID'], i['SUB_GENE'], \
    			i['SUB_MOD_RSD'], i['SITE_GRP_ID'], i['SITE_7_AA'] ) for i in dr_2]

cur.executemany("INSERT INTO Kinase_Phosphosite(Keys_,GENE, KINASE, KIN_ACC_ID, SUBSTRATE, SUB_ACC_ID, SUB_GENE,\
				 SUB_MOD_RSD, SITE_GRP_ID, SITE_7_AA) VALUES (?,?,?,?,?,?,?,?,?,?);", to_db_2)

con.commit()

print to_db_2



### 5: TO JOIN THE TABLES USING A FOREIGN KEY

cur.execute("SELECT Name FROM Kinase_Information INNER JOIN Kinase_Phosphosite ON Kinase_Phosphosite.GENE = Kinase_Information.Name ;") 


print(cur.fetchall())

con.commit()


##THE CONNECTION MUST BE CLOSED AT THE END

con.close()