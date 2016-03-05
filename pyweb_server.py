from tools.config import config_options
import boot
import modules

# flask server
from modules.flask_app import web_path

if config_options.log_level == "DEBUG":
    web_path.debug = True

web_path.run()
