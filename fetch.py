from lxml import html
import json
import re
from request import request
from urllib.parse import urljoin



def get_page_data(url):
    data = request(url)
    tree = html.fromstring(data)

    script = tree.xpath('//script[contains(text(),"__INITIAL_STATE__")]')

    script_text = script[0].text

    match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script_text, re.DOTALL)

    json_text = match.group(1)

    return json_text

def urls(page_data):
    base_url="https://www.espn.in/"

    data_json=json.loads(page_data)
    
    all_matches=[]
    for a in data_json.get('scoreboard').get('leagues'):
        for j in a.get('events'):
            all_matches.append({
                'date':j.get('date'),
                'match':j.get('teams').get('gameInfo'),
                'score':"".join(urljoin(base_url,i.get('href')) for i in j.get('links') if i.get('text')=='Scorecard')
            })
    return all_matches