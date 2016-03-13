from tools.config import config_options
import boot
import modules


extra_files = ['modules/static/less/build.less', 'modules/static/less/custom.less']
# flask server
from modules.flask_app import web_path

if config_options.log_level == "DEBUG":
    web_path.debug = True


web_path.run(extra_files=extra_files)
