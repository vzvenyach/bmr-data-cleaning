import lib.check_db as checkdb
from lib.get_code_from_usda_api import get_code_from_usda_api
import sqlite3
import time
import pdb

sqlite_file = 'usda.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("SELECT * FROM usda_codes WHERE USDA_ID == 'UNKNOWN'")
results = c.fetchall()

for row in results:
    res = c.execute("SELECT * FROM usda_codes WHERE FOOD_DESCRIPTION == ? AND USDA_ID != 'UNKNOWN';", (row[1],)).fetchone()
    if res is not None:
        c.execute("DELETE FROM usda_codes WHERE food_description == ? AND usda_id == 'UNKNOWN';", (row[1],))
        conn.commit()
        # pdb.set_trace()
