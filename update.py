from wpupdater.WPBlog import WPBlog
from wpupdater.SeoChecker import *
from wpupdater.utils import LoginException, WPLoggerAdapter, check_for_new_version, parse_config
import urllib2
import datetime
import logging
import signal
import sys
import socket
import os


CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/config.cfg')
logging_levels = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO
                  }

def main():

    result = {
            'updated': 0,
            'up-to-date': 0,
            'update_errors': 0,
            'login_errors': 0,
            'connection_errors': 0
            }

    def print_result(result):
        print "\n\n\n Updated: %(updated)s \n Up-to-date: %(up-to-date)s \n Update Errors: %(update_errors)s \n Login Errors: %(login_errors)s \n Connection Errors: %(connection_errors)s"%(result)

    def sigint_handler(*args):
        print print_result(result)
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)

    config = parse_config(CONFIG_FILE)



    # Logger setup
    logger = logging.getLogger(config.get('logger','name'))
    logger.setLevel(config.get('logger', 'log_level'))
    formatter = logging.Formatter(config.get('logger', 'format', raw=True))
    fh = logging.FileHandler(config.get('logger', 'log_file'))
    ch = logging.StreamHandler()
    fh.setLevel(logging_levels.get(config.get('logger', 'log_level'), logging.INFO))
    ch.setLevel(logging_levels.get(config.get('logger', 'console_level'), logging.INFO))
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('WPUpdater started\n===========================\n\n\n')
    if not check_for_new_version():
        logger.info("No new versions of WP, exiting...")
        sys.exit(0)

    # Database setup
    db = Database(host=config.get('database', 'host'), username=config.get('database', 'username'), password=config.get('database', 'password'), dbname=config.get('database', 'name'))


    # Get domain manager
    domain_manager = Domain(db, config.get('database', 'sql', raw=True))

    for wp in domain_manager.get_wp_list():
        log_adapt = WPLoggerAdapter(logger, {'domain': wp['url']})
        start_time = datetime.datetime.now()
        blog = WPBlog(wp['url'], wp['wp_login'], wp['wp_pass'])
        log_adapt.debug('Opening ')
        try:
            blog.login()
            version = blog.get_current_version()
            #plugins = blog.get_plugin_updates_count()
            is_upgradeable = blog.check_if_upgradeable()
            log_adapt.debug('\t ->Logged in, checking current version...')
            if not is_upgradeable:
                log_adapt.info('\t ->Current version is %s, up-to-date'%(version))
                result['up-to-date'] += 1
            else:
                log_adapt.info('\t -> \033[92m Current Version = %s, is upgradeable \033[0m'%(version))
                log_adapt.info('\t ->Upgrading....')
                if blog.upgrade():
                    log_adapt.info("\t\t \033[92m -> UPGRADED! \033[0m")
                    result['updated'] += 1
                else:
                    log_adapt.error("\t\t \033[91m -> UPGRADE ERROR!\033[0m")
                    result['update_errors'] += 1
        except LoginException as e:
            log_adapt.error("\t \033[91m -> Login Error! \033[0m")
            result['login_errors'] += 1
        except urllib2.URLError:
            log_adapt.error("\t \033[91m -> Error Opening! \033[0m")
            result['connection_errors'] += 1
        except Exception as e:
            log_adapt.error("UNKNOWN ERROR %s"%e)
        stop_time = datetime.datetime.now()
        log_adapt.info("Ended up in %s seconds\n"%((stop_time - start_time).total_seconds()))
    print_result(result)

if __name__ == "__main__":
    main()
