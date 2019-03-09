import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://www.thegradcafe.com/survey/index.php?q=Brown+University+computer+science&t=a&o=&p=1'

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

t_rows = soup.body.main.findAll('section', {'class': 'submissions'})[0].div.table.findAll('tr')

print(soup.body.main.table)

pass
