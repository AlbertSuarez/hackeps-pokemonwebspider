import random
import requests

from bs4 import BeautifulSoup

from src import *


def _scrape_pokemon():
    # Retrieve PokemonDB HTML
    response = requests.get(SCRAPE_POKEMON_HTML, verify=False, timeout=15)
    assert response.ok
    html_content = response.content

    # Create BS4 object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Scrape pokedex list
    pokedex_table = soup.find('table', {'id': 'pokedex'})
    pokedex_list = pokedex_table.find_all('tr')
    pokedex_list = pokedex_list[1:]  # Remove header

    # Save data
    pokedex_result = []
    for row in pokedex_list:
        row_type = row.find_all('a', {'class': 'type-icon'})
        if len(row_type) == SCRAPE_POKEMON_MIN_TYPE:
            row_img = row.find('span', {'class': 'infocard-cell-img'})
            row_num = row.find('span', {'class': 'infocard-cell-data'})
            row_name = row.find('a', {'class': 'ent-name'})
            pokedex_result.append({
                'name': row_name.text,
                'number': row_num.text,
                'img': row_img.next['data-src'],
                'type': [row_type[0].text, row_type[1].text]
            })

    # Ger random values
    pokedex_team = []
    for _ in range(0, SCRAPE_POKEMON_AMOUNT):
        while True:
            pokedex_item = random.choice(pokedex_result)
            if all([i for i in pokedex_team if i['type'] != pokedex_item['type']]):
                pokedex_team.append(pokedex_item)
                break

    return pokedex_team


def _render_template(pokedex_team):
    with open(HTML_TEMPLATE_PATH, 'r', encoding='utf-8') as template_html_file:
        template_html_string = template_html_file.read()

    for idx, pokedex_item in enumerate(pokedex_team):
        print('Number: {}\tName: {}\tType: {}\tImg: {}\t\n'.format(
            pokedex_item['number'], pokedex_item['name'], pokedex_item['type'], pokedex_item['img'])
        )
        template_html_string = template_html_string.replace(f'data.number_{idx + 1}', pokedex_item['number'])
        template_html_string = template_html_string.replace(f'data.name_{idx + 1}', pokedex_item['name'])
        template_html_string = template_html_string.replace(f'data.img_{idx + 1}', pokedex_item['img'])
        template_html_string = template_html_string.replace(f'data.type_{idx + 1}', '/'.join(pokedex_item['type']))

    with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as output_html_file:
        output_html_file.write(template_html_string)


def generate():
    pokedex_team = _scrape_pokemon()
    _render_template(pokedex_team)
