from pathlib import Path
from jinja2 import Template
from yaml import load_all

supported_languages = set()

with open(Path(__file__).parent/'CodeStyle.yaml') as file:
    syntax, CONDITIONS, SNIPPETS = load_all(file)

for lang, values in syntax.items():
    for key, value in values.items():
        syntax[lang][key] = Template(value)
SYNTAX = syntax

__all__ = ('supported_languages', 'SYNTAX', 'CONDITIONS', 'SNIPPETS')
