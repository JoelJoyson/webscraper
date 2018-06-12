###########Code to scrap Wiki's page and get data then insert into Mysql table"
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import csv
from datetime import datetime
from sqlalchemy import create_engine


#specify the url

wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"
#Query the website and return the html to the variable 'page'
page = urllib2.urlopen(wiki)

#Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page,'html.parser')
#print soup.prettify();
print soup.title;
print soup.find_all("a");

all_links=soup.find_all("a")
for link in all_links:
        print link.get("href")
all_tables=soup.find_all("table")

right_table=soup.find('table', class_='wikitable sortable plainrowheaders')
print right_table

A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
for row in right_table.findAll("tr"):
    cells = row.findAll('td')
    states=row.findAll('th') #To store second column data
    if len(cells)==6: #Only extract table body not heading
        A.append(cells[0].find(text=True))
        B.append(states[0].find(text=True))
        C.append(cells[1].find(text=True))
        D.append(cells[2].find(text=True))
        E.append(cells[3].find(text=True))
        F.append(cells[4].find(text=True))
        G.append(cells[5].find(text=True))

        desired_width = 600
        pd.set_option('display.width', desired_width)
pd.set_option("display.max_columns",100)

df=pd.DataFrame(A,columns=['Number'])
df['State/UT']=B
df['Admin_Capital']=C
df['Legislative_Capital']=D
df['Judiciary_Capital']=E
df['Year_Capital']=F
df['Former_Capital']=G

print df

with open('capital_data .csv', 'a') as csv_file:
 writer = csv.writer(csv_file)
 writer.writerow([df, datetime.now()])

# To write t mysql db
con=create_engine('mysql+mysqldb://root:root@127.0.0.1/mytest',convert_unicode=True);
df.to_sql(con=con,name='country_info',if_exists='append');
