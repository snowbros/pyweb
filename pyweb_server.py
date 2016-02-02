from tools.config import config_options
import modules

#flask server
from modules.flask_app import web_path

web_path.debug = True
web_path.run()

