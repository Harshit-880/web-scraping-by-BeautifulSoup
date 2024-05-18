from bs4 import BeautifulSoup
import requests
import json
import openpyxl

# have to pass the path of the excel file which contain url
# to run you have to change the path from your local path of excel file
excel_file = "c:\\Users\\garga\\Downloads\\Scrapping Python Assigment- Flair Insights.xlsx" 

workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active

# contain all urls of the excel file 
urls = []

for row in sheet.iter_rows(values_only=True):
    url = row[0]
    urls.append(url)

all_scraped_data = []

# iteratte to only 10 index to save from error
for i in range(10):
    print("Scraping data from:", urls[i])
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    scraped_data = {'url': url, 'text': [], 'images': [], 'links': []}

    text_elements = soup.find_all(text=True)
    scraped_data['text'] = [element.strip() for element in text_elements if element.strip()]

    image_tags = soup.find_all('img')
    scraped_data['images'] = [img['src'] for img in image_tags if 'src' in img.attrs]

    link_tags = soup.find_all('a')
    scraped_data['links'] = [link['href'] for link in link_tags if 'href' in link.attrs]

    all_scraped_data.append(scraped_data)


# this code store all the data in json formate and file will create by running command python test.py
output_file = 'all_scraped_data.json'
with open(output_file, 'w') as json_file:
    json.dump(all_scraped_data, json_file, indent=4)

print("All scraped data has been stored in", output_file)
