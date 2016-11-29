import sqlite3
sqlite_file = 'usda.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# check if food_code present

def check_database_for_id(food_code, food_description):
    # food_code = 215469
    if food_code != '':
        data = c.execute("SELECT * FROM usda_codes WHERE food_id = ?;", (food_code,)).fetchone()
    else:
        data = c.execute("SELECT * FROM usda_codes WHERE food_description = ?;", (food_description,)).fetchone()
    if data is None:
        return None
    return (data[1], data[2])

def insert_code_into_usda_api(food_code, food_description, results):
    c.execute("INSERT INTO USDA_CODES(FOOD_ID, FOOD_DESCRIPTION, USDA_ID, USDA_DESCRIPTION) VALUES (?, ?, ?, ?);", (
        food_code,
        food_description,
        results[0],
        results[1],
    ))
    conn.commit()
    return True
