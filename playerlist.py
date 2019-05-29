#Importing all the necessary packages
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv

#Requests the web-page to open and store it in the variable
def request_html(url):
    request = urlopen(url)
    html_page = request.read()
    request.close()
    
    soup_html = soup(html_page, "html.parser")
    
    return soup_html
    
#Url from which we scrape the data
url = "https://en.wikipedia.org/wiki/List_of_Afghanistan_ODI_cricketers"

html_page = request_html(url)

#Find all the li elements where qoutes are present
table = html_page.findAll('table', {'class','wikitable'})

links = table[0].findAll('span', {'class','vcard'})
names = []

for link in links:
    name_link = link.find('a')
    name = name_link.string
    names.append(name)

with open('afg_players.csv', 'w') as file:
    writer = csv.writer(file, delimiter=',', lineterminator='\n')
    for name in names: writer.writerow([name])

file.close()
