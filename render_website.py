import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('meta_data.json', encoding='utf-8') as file:
        books = json.load(file)

    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)


if __name__ == '__main__':
    on_reload()

    server = Server()

    server.watch('template.html', on_reload)
    server.watch('meta_data.json', on_reload)

    server.serve(root='.')