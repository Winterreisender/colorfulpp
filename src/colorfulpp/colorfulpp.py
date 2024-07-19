import os
import sqlite3
from pathlib import Path
from dataclasses import dataclass
import csv
import json
from typing import Iterator

BASE_DIR=Path(".")

@dataclass
class Entry:
    id    :str
    name  :str
    color :str
    description :str = ''

    def to_sql(self):
        return f"'{self.id}', '{self.name}', '{self.color}', '{self.description}'"

    # Some simple ORM
    @classmethod
    def from_sql(cls, sql_data):
        return Entry(*map(str, sql_data))
    
    def to_css(self):
        return """
/* %s */
#%s {
    --theme: %s;
    background: var(--theme);
    color: var(--theme);
}""" % (self.name, self.id, self.color)

class Table:
    def __init__(self, cur :sqlite3.Cursor, table_name :str, name :str | None = None) -> None:
        self.cur = cur
        self.id = table_name
        self.name = name if name else table_name
    
    def add_entry(self, entry :Entry):
        self.cur.execute(f"INSERT INTO {self.id} (id, name, color, description) VALUES ({entry.to_sql()})")

    def __iter__(self) -> Iterator[Entry]:
        self.cur.execute(f"select * from {self.id}")
        for i in self.cur.fetchall():
            yield Entry.from_sql(i)

    def show(self):
        self.cur.execute(f"select * from {self.id}")
        for i in self.cur.fetchall():
            print(Entry.from_sql(i))

    def import_csv(self, path :Path):
        with open(path, 'r', encoding='utf-8') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            for row in reader:
                self.add_entry(Entry(*row))


    def to_html(self):
        css = ''
        html = ''
        for i in self.__iter__():
            css += i.to_css()
            html += f"<div id='{i.id}' class='card'><p>{i.name}</p><p>{i.color}</p></div>"

        return """
            <html>
            <head>
                <title>Colorfulpp</title>
                <style>%s</style>
                <style>
                    main {
                        display: flex;
                        flex-flow: row wrap;
                    }
                    .card {
                        width: 9vw;
                        height: 9vh;
                        margin: 1vh 1vw;
                    }
                    .card p {
                        margin: 0;
                        padding: 0;
                        color: currentColor;
                        filter: grayscale(1) contrast(999) invert(1)
                    }
                    header h1 {
                        display: inline;
                    }
                </style>
            </head>
            <body>
                <header>
                    <h1>%s</h1> <code>%s<code>
                </header>
                <main>
                    %s
                </main>
            </body>
            </html>
        """ % (css, self.name, self.id,html)
    
    
# singleton
class _Db:
    def __init__(self, path :Path = BASE_DIR / "data/default.db") -> None:
        os.makedirs(path.parent, exist_ok=True)
        self.con = sqlite3.connect(path)
        self.cur :sqlite3.Cursor = self.con.cursor()

    def all_table(self) -> list[str]:
        self.cur.execute("SELECT tbl_name FROM sqlite_master WHERE type IN('table', 'view') AND name NOT LIKE 'sqlite_%';");
        return [x[0] for x in self.cur.fetchall()]

    def drop_table(self, tbl_name):
        self.cur.execute(f"DROP TABLE '{tbl_name}'")

    def create_table(self, tbl_name :str, name=None, /,drop_if_exists = False):
        assert (not tbl_name.startswith("sqlite_")) and (not tbl_name.endswith("_meta"))
        self.cur.execute(f"DROP TABLE IF EXISTS {tbl_name}") if drop_if_exists else None
        self.cur.execute(f"CREATE TABLE {tbl_name} (id CHAR(64) PRIMARY KEY NOT NULL, name TEXT, color TEXT, description TEXT)")
        return Table(self.cur, tbl_name)

    def create_table_from_json(self, jsonpath :Path, drop_if_exists = False):
        name,tbl_name,description = '', '', ''
        with open(jsonpath, 'r', encoding='utf-8') as jsonfile:
            d = json.load(jsonfile)
        name,tbl_name,description = d['name'], d['id'], d['description']

        table = self.create_table(tbl_name, name, drop_if_exists)

        for i in d['colors']:
            table.add_entry(Entry(**i))

        return table

    def __del__(self):
        self.con.commit()
        self.con.close()

        

db = _Db()