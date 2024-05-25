import requests
from tqdm import tqdm 
from thefuzz import fuzz
from bs4 import BeautifulSoup
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


input_path = r'C:\Users\ignore\Desktop\Reference.bib'
output_path = r'C:\Users\ignore\Desktop\Reference_new.bib'

with open(input_path, encoding='utf-8') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

new_entries = []
for entry in tqdm(bib_database.entries):
    title = entry['title'].replace("{","").replace("}","")
    if 'bibsource' in entry and 'dblp' in entry['bibsource']:
        new_entries.append(entry)
        continue
    # search 
    base_url = 'https://dblp.org/search'
    output = requests.get(base_url, params={"q":title})
    soup = BeautifulSoup(output.text, 'html.parser')
    res = soup.find_all('ul',{'class':'publ-list'})[0]
    all_item = res.find_all('li',{"itemtype":"http://schema.org/ScholarlyArticle"})

    bibtex_url = None
    for item in all_item:
        new_title = item.find_all('span',{"class":"title"})[0].text
        new_url = item.find_all('a',{"rel":"nofollow"})[0]['href']
        if fuzz.ratio(new_title.lower(), title.lower()) >= 90:
            bibtex_url = new_url
            break
    if bibtex_url is None or 'bibtex' not in bibtex_url:
        print(f'`{title}` not find!')
        new_entries.append(entry)
        continue

    # get bibtext
    output = requests.get(bibtex_url)
    soup = BeautifulSoup(output.text,'html.parser')
    tex_str = soup.find_all('pre',{'class':'verbatim select-on-click'})[0].text
    new_entry = bibtexparser.loads(tex_str).entries[0]
    
    new_title = new_entry['title']
    new_entry['ID'] = entry['ID']
    new_entries.append(new_entry)


db = BibDatabase()
db.entries = new_entries
writer = BibTexWriter()
with open(output_path, 'w', encoding='utf-8') as bibfile:
    bibfile.write(writer.write(db))