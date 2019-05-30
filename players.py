#Importing all the necessary packages
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd

#Requests the web-page to open and store it in the variable
def request_html(url):
    request = urlopen(url)
    html_page = request.read()
    request.close()
    
    soup_html = soup(html_page, "html.parser")
    
    return soup_html
    
#Url from which we scrape the data
url = "https://en.wikipedia.org/wiki/List_of_One_Day_International_cricketers"

html_page = request_html(url)
team_names_list = html_page.findAll('h2')
team_names = []

for el in team_names_list[1:-1]:
    temp = el.findAll('span')
    team_names.append(temp[0].get('id'))

player_link_list = html_page.find_all('p')

#Removing the first 'p'
player_link_list.pop(0)
player_links=[]
player_names=[]

for el in player_link_list:
    temp_links = el.small.find_all('a')
    player_links.append(temp_links)

#For loop for scraping the player names
for el in player_links:
    player_temp_names=[]
    for link in el:
        ntemp = link.get_text()
        player_temp_names.append(ntemp)
    
    player_names.append(player_temp_names)
    
#Appending the team names to the beginning of every list
full_temp_list = list(zip(team_names, player_names))
full_list = []

for el in full_temp_list:
    temp = list(el).copy()
    temp[1].insert(0, temp[0])
    temp.pop(0)
    full_list.append(temp)

#Flatting the list
full_flat_list = []

for x in full_list:
    for el in x:
        full_flat_list.append(el)

#Exporting the list to CSV file using DataFrame
df = pd.DataFrame(full_flat_list)
df.to_csv('player_names.csv', index=False, header=False)
