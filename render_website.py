import json
import os
import math
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

BOOKS_ON_PAGE = 10


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('meta_data.json', encoding='utf-8') as file:
        books = json.load(file)


    os.makedirs('pages', exist_ok=True)
    pages = list(chunked(books, BOOKS_ON_PAGE))

    for page_number, books_on_page in enumerate(pages, start=1):
        books_in_columns = list(chunked(books_on_page, 2))

        rendered_page = template.render(
            books_in_columns=books_in_columns,
            current_page=page_number,
            pages_count=len(pages)
        )

        with open(f'pages/index{page_number}.html', 'w', encoding='utf-8') as file:
            file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.watch('meta_data.json', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()