import requests as r
import pandas as pd
import bs4 as bs

def get():

    for i in range(1,126):
        resp = r.get(f"http://www.yougowords.com/7-letters-{i}")
        df = pd.read_html(resp.content)
        df[0].to_csv('seven.csv',mode='a', index=False, header=False)

def analyse():
    d = pd.read_csv('seven.csv')
    #x = d['Origin'].unique()
    y = d[(d['Origin'] == 'Middle English') | ( d['Origin'] == 'Old English')].Word
    y.str.upper().to_csv('English-7.csv', header=False, index=False)

def get_definition():
    with open('English-5.csv', encoding='UTF-8') as f:
        wrds = f.readlines()
    definitions = {}

    cnt = 1
    for wrd in wrds:
        resp = r.get(f"https://www.onelook.com/?w={wrd}")
        c = resp.content
        soup = bs.BeautifulSoup(c,'lxml')
        
        try:
            p = soup.find('span',{'id':'easel_def__0'}).text
        except:
            p = '[No defintion found.]'

        definitions.update({wrd.replace('\n',''):p})
        cnt = cnt + 1
        print(cnt)
    
    defs = pd.DataFrame.from_dict(definitions, orient='index')
    defs.to_csv('English-5-defs.csv', header=False, index=False)
        




get_definition()