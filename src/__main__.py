import os
import subprocess
import tempfile
from colorfulpp.colorfulpp import Table, Entry, db
import argparse
import sys
import platform
import click

def startfile(file_path):
    match sys.platform:
        case 'win32' | 'mingw':
            os.startfile(file_path)
        case 'linux' | 'freebsd':
            subprocess.call(["xdg-open",file_path])
        case 'darwin':
            subprocess.call(["open", file_path])

@click.group()
def cli():
    pass

@cli.command()
def table_list():
    for i in db.all_table():
        print(i)

@cli.command()
@click.argument('table_name')
def color_list(table_name :str):
    table = Table(db.cur, table_name)
    for i in table:
        print(f"{i.id}\t{i.name}\t{i.color}")

@cli.command()
@click.argument('table_name')
def table_show(table_name :str):
    table = Table(db.cur, table_name)
    s = table.to_html()
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmpfile:
        tmpfile.write(s.encode())
    startfile(tmpfile.name)

@cli.command()
@click.argument('json_path')
@click.option("--force",  default=False, is_flag=True)
def table_import(json_path, force :bool):
    db.create_table_from_json(json_path, bool(force))

@cli.command()
@click.argument('table_name')
def table_remove(table_name :str):
    db.drop_table(table_name)

if __name__=="__main__":
    cli()