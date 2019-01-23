import requests
from bs4 import BeautifulSoup

url="http://kinase.com/web/current/kinbase/genes/SpeciesID/9606/"

res = requests.get(url)
lst = []
count = 0
string = ""
soup = BeautifulSoup(res.text, "lxml")
for items in soup.select(".table tr"):
    data = ([' '.join(item.text.split()) for item in items.select("th,td")])
    if count==0:
        count+=1
        continue
    string = string + ''.join(data[4].split(","))
    string = string.replace(" ","\n")+"\n"
    lst.append(data[4].split(","))
output=open("output.txt","w")
output.write(string)
print("output.txt is generated successfully..!")