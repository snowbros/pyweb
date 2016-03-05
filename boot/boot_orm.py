from tools.config import config_options
from orm import db

# this variable hold value wether server run first time
new_born = not db._table_exist("system_info")

if new_born:
    db._create_table("system_info")
    db._commit()
