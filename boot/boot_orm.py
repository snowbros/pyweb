from tools.config import config_options
from orm import db
import os
import subprocess

import logging

logger = logging.getLogger(__name__)


# this variable hold value wether server run first time
new_born = not db._table_exist("system_info")

if new_born:
    db._create_table("system_info")
    db._commit()

cwd = os.getcwd()
source = cwd + '/modules/static/less/build.less'
dest = cwd + '/modules/static/css/bootstrap.css'
try:
    subprocess.Popen(['lessc', source, dest])
    logger.info("New Less compiled")
except:
    logger.error("Error in less compile")
