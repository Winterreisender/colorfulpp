import os
from pathlib import Path
import tempfile
import unittest
import sqlite3

from colorfulpp.colorfulpp import Entry, Table, db

BASE_DIR=Path(".")

class DemoTestCase(unittest.TestCase):
    def setUp(self):
        self.table1 = db.create_table_from_json(BASE_DIR/'data/nippon_colors.json', drop_if_exists=True)

    def test_css(self):
        entry = Entry("red", "红", "#ff0000")
        print(entry.to_css())
    
    def test_html(self):
        s = self.table1.to_html()
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmpfile:
            tmpfile.write(s.encode())
        
        os.startfile(tmpfile.name) # windows only. linux上可以使用subprocess.call(["xdg-open",file_path]) macos上使用subprocess.call(["open", file_path])


    def tearDown(self) -> None:
        self.con.commit()
        self.con.close()
        return super().tearDown()

if __name__=="__main__":
    unittest.main() 