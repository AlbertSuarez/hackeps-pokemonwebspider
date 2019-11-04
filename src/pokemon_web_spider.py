from src import *


def _scrape_pokemon():
    pass


def _render_template():
    with open(HTML_TEMPLATE_PATH, 'r', encoding='utf-8') as template_html_file:
        template_html_string = template_html_file.read()

    # TODO

    with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as output_html_file:
        output_html_file.write(template_html_string)


def generate():
    _scrape_pokemon()
    _render_template()
