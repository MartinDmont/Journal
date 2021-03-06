from cryptography.fernet import Fernet
import os
import configparser
def Henri_reinit():
    confi = configparser.ConfigParser()
    with open("henri.key",'wb') as logger:
        key = Fernet.generate_key()
        logger.write(key)
        
    cipher_suite = Fernet(key)
    dico = {
        'host' : str(cipher_suite.encrypt(b"SECRET")),
        'database' : str(cipher_suite.encrypt(b"SECRET")),
        'user' : str(cipher_suite.encrypt(b"SECRET")),
        'port' : str(cipher_suite.encrypt(b"SECRET")),
        'password' : str(cipher_suite.encrypt(b"SECRET"))
    }

    for x in dico:
        confi["DATAS"] = dico
    
    with open("config.ini",'w') as configfile:
        confi.write(configfile)

def getkey():
    global key
    with open('henri.key','rb') as logger:
        key = logger.read()
    return key