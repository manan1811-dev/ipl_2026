from request import request
from fetch import get_page_data, urls
from lxml import html
import json
from db import create_tabel, insert_single_match, match_url_exists

print("Script started")

main_url = 'https://www.espn.in/cricket/scores/series/8048/season/2026/indian-premier-league'

create_tabel()

href = get_page_data(main_url)
all_matches = urls(href)

count = 0
full_details = []

for a in all_matches:
    data = a.get('score')

    if not data:
        continue

    if match_url_exists(data):
        continue

    try:
        print(f"Processing: {data}")
        response = request(data)
        final_data = get_page_data(data)
        match_response = json.loads(final_data)

        game_package = match_response.get('gamePackage', {})

        all_data = game_package.get('scorecard', {}).get('innings', {})
        teams = game_package.get('gameStrip', {}).get('teams', {})

        match_data = {
            'match': a.get('match'),
            'date': a.get('date'),
            'winner': game_package.get('summary'),

            'score': {
                teams.get('home', {}).get('name'): teams.get('home', {}).get('score'),
                teams.get('away', {}).get('name'): teams.get('away', {}).get('score')
            },

            'match_url': data,
            'innings': {}
        }

        if match_data['winner']:

            for k, v in all_data.items():

                match_data['innings'][k] = {
                    'team': v.get('title'),

                    'batsmen': {
                        b.get('displayName'): {
                            s.get('name'): s.get('value')
                            for s in b.get('stats', [])
                        }
                        for b in v.get('batsmen', [])
                        if b.get('displayName')
                    },

                    'bowlers': {
                        b.get('displayName'): {
                            s.get('name'): s.get('value')
                            for s in b.get('stats', [])
                        }
                        for b in v.get('bowlers', [])
                        if b.get('displayName')
                    }
                }

            insert_single_match(match_data)

            full_details.append(match_data)
            count += 1
            print(f"Inserted Match: {count}")
            print("Script finished")

        else:
            break

    except Exception as e:
        print(f"Error processing match: {data}")
        print(e)
        continue


with open('all_match.json', 'w', encoding='utf-8') as f:
    json.dump(full_details, f, indent=4, ensure_ascii=False)

print("Done!!!") 