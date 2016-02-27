import argparse


def get_configs():
    #Command line argument parser
    config_parser = argparse.ArgumentParser()

    #General Options
    general_group = config_parser.add_argument_group('General')
    general_group.add_argument('-no-static',
                               action='store_false', default=True, dest='load_static_dir',
                               help="Don't load static folder")
    general_group.add_argument('--log-level',
                                action='store', dest='log_level', default="DEBUG",
                                help='Define log level DEBUG, INFO etc')

    #Database related option
    db_options = config_parser.add_argument_group('Database')
    db_options.add_argument('--db-name',
                            action='store', dest='db_name',
                            help='Database Name')
    db_options.add_argument('--updata-schema',
                            action='store_true', default=False, dest='update_schama',
                            help="Update Database Schema (Re-compute-orm)")
    args = config_parser.parse_args()
    return args

config_options = get_configs()
