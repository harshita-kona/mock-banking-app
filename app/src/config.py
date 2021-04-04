from os import getenv
config_obj = {}
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.curdir, 'app/src/config_files/.env')))

def init_config():
    """
    Read environment variables and set appropriate keys in the config object
    """
    global config_obj
    
    config_obj['api_key'] = getenv('API_KEY', 'NEEDKEYHERE')

    config_obj['postgres_conf'] = {
        "pg_host": getenv('PG_HOST',''),
        "pg_port":getenv('PG_PORT', 0),
        "pg_user": getenv('PG_USER',''),
        "pg_pw": getenv('PG_PASSWORD',''),
        "pg_database": getenv('PG_DB',''),
    }

    config_obj['email_conf'] = {
        "mail_host": getenv('GHOST',''),
        "mail_port":getenv('GPORT', ''),
        "mail_user": getenv('GHOSTU',''),
        "mail_pw": getenv('GHOSTP',''),
        "contact_recp": getenv('CONTACT_RECIPIENTS',''),
        "error_recp": getenv('ERROR_RECIPIENTS',''),
    }

    config_obj['key']=getenv('SECRET_KEY','')
    config_obj['algorithm']=getenv('ALGORITHM','')
    config_obj['expire_token']=getenv('ACCESS_TOKEN_EXPIRE_MINUTES','')

    return config_obj

def get_config():
    global config_obj
    if len(config_obj) == 0:
        init_config()
    return config_obj
