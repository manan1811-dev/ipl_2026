from request import *
from fetch import *
from lxml import html
import json
from db import *

main_url='https://www.espn.in/cricket/scores/series/8048/season/2026/indian-premier-league'

create_tabel()
existing_urls = {i['match_url'] for i in fetch_match_url()}
href=get_page_data(main_url)

count=0
all_matches=urls(href)
full_details=[]
for a in all_matches:
    data=a.get('score')
    if not data or data in existing_urls:
        continue
    response=request(data)
    final_data=get_page_data(data)
    match_responce=json.loads(final_data)
    
    all_data = match_responce.get('gamePackage').get('scorecard').get('innings')
    teams = match_responce.get('gamePackage').get('gameStrip').get('teams')
    match_data ={
        'match':a.get('match'),
        'date':a.get('date'),
        'winner':match_responce.get('gamePackage').get('summary'),
        'score':{
            teams.get('home').get('name'):teams.get('home').get('score'),
            teams.get('away').get('name'):teams.get('away').get('score')
        },
        'match_url':data,
        'innings':{}
    }
    if match_data['winner']:
        for k,v in all_data.items():
            match_data['innings'][k] = {
                'team':v.get('title'),
                'batsmen':[{
                    'batsman_name':b.get('displayName'),
                    'all_stats':{s.get('name'):s.get('value') for s in b.get('stats')}
                } for b in v.get('batsmen')],
                'bowlers':[{
                    'bowlers_name':b.get('displayName'),
                    'all_stats':{s.get('name'):s.get('value') for s in b.get('stats')}
                } for b in v.get('bowlers')]
            }
        insert_single_match(match_data)
        full_details.append(match_data)
        count+=1
        print(count)
    else:
        break    

with open('all_match.json','w',encoding='utf-8') as f:
    json.dump(full_details,f,indent=4,default=str)