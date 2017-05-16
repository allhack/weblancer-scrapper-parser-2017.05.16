import csv
import requests
from bs4 import BeautifulSoup
#https://www.weblancer.net/jobs/?page=2
base_url = "https://www.weblancer.net/jobs/"
projects = []
r = requests.get(base_url)
soup = BeautifulSoup(r.content, 'html.parser')
pages = soup.find('ul', {'class': 'pagination'})
pages = int(pages.contents[len(pages.contents)-1].contents[0].get('href')[12:])

for page in range(1, pages):
    url = base_url + '?page=' + str(page)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    g_data = soup.find_all('div', {'class': 'container-fluid cols_table show_visited'})
    g_data = g_data[0].find_all('div', {'class': 'row'})
    for item in g_data:
        title = item.contents[0].text.strip()
        if item.contents[1].text.strip() == '':
            amount = '-'
        else:
            amount = item.contents[1].text.strip()
        apps = item.contents[2].text.strip()
        projects.append({
            'title': title,
            'amount': amount,
            'apps': apps
        })

with open('list.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('Название', 'Цена', 'Заявки'))
    for project in projects:
        writer.writerow((project['title'], project['amount'], project['apps']))

#print(projects)