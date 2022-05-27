import click
from . import pydoc_formatter

@click.command()
@click.argument('filenames', nargs=-1)
def fix_D400(filenames):
    for filename in filenames:
        pydoc_formatter.format_file_d400(filename)