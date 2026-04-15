from lxml import html
import requests as re

def request(url):
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'referer':'https://www.espn.in/cricket/series/_/id/8048/season/2025/indian-premier-league'
    }

    responce=re.get(url,headers=headers)
    
    if responce.status_code==200:
        return responce.text
    else:
        print("Error!!!")