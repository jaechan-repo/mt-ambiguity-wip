#This will not run on online IDE
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

database = pd.DataFrame(columns=["idiom", "meaning", "example"])
LAST_PAGE = 156
for i in range(1, LAST_PAGE + 1):
    try:
        URL = f"https://www.theidioms.com/list/page/{i}/"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
        dl = soup.find('dl')
        dt = [t.text for t in dl.find_all('dt')]
        dd = [t.text for t in dl.find_all('dd')]
        dt = [t.replace('’', "\'") for t in dt]
        dd = [t.replace('’', "\'") for t in dd]
        dd = [re.sub(" Read on$", "", t) for t in dd]
        meanings = [re.search(r'(?<=Meaning: )(.*)(?=Example:)', t).group(1) for t in dd]
        examples = [re.search(r'(?<=Example: )(.*)(?=$)', t).group(1) for t in dd]
        df = pd.DataFrame(list(zip(dt, meanings, examples)), columns=["idiom", "meaning", "example"])
        database = pd.concat([database, df])
    except:
        continue
database.to_csv('idioms.csv', index=False)