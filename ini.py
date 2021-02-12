import configparser

ini = configparser.ConfigParser()
ini.read('config.ini', encoding='UTF-8')

ini_user = ini['db_info']['user']
ini_pass = ini['db_info']['password']
ini_host = ini['db_info']['host']
ini_db = ini['db_info']['database']

ini_key = ini['secret_key']['sec_key']
