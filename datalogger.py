import config
import psycopg2
import configparser
from cryptography.fernet import Fernet


class Logger(object):
    def __init__(self):
        self.key = config.getkey()
    
    def flower(self,table):
        f = Fernet(self.key)
        config = configparser.ConfigParser()
        config.read('config.ini')
        database = config["DATAS"]["database"]
        params = []
        for x in config["DATAS"]:
            y = bytes(config["DATAS"][x][2:],'utf-8')
            params.append(str(f.decrypt(y))[2:-1])
        
        print(f"dbname = {params[1]},host = {params[0]},user = {params[2]},password = {params[4]}")
        con = psycopg2.connect(dbname = params[1],host = params[0],user = params[2],password = params[4])
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM {table}""")
        rows = cur.fetchall()
        liste = []
        for r in rows:
            liste.append([str(r[i]) for i in range(len(cur.description))])
        
        return liste

    def insert_cry(self,table,dict_of):
        dico = dict_of
        f = Fernet(self.key)
        config = configparser.ConfigParser()
        config.read('config.ini')
        database = config["DATAS"]["database"]
        params = []
        for x in config["DATAS"]:
            y = bytes(config["DATAS"][x][2:],'utf-8')
            params.append(str(f.decrypt(y))[2:-1])
        con = psycopg2.connect(dbname = params[1],host = params[0],user = params[2],password = params[4])
        cur = con.cursor()
        keys = ""
        values = ""
        for i in dict_of.keys():
            keys = keys + f"""{i},"""
        for i in dict_of.values():
            if str(i).startswith("["):
                i = i.strip('][').split(',') 
                values = values + "["
                for y in range(len(i)) :
                    truc = i[y]
                    if y != len(i):
                            values = values + "'"+str(f.encrypt(bytes(truc,'utf-8')))[2:-1] + "',"
                    else:
                        values = values + "'"+str(f.encrypt(bytes(truc,'utf-8')))[2:-1]
                values =  values + "],"
            else:
                values = values + f"""'{str(f.encrypt(bytes(i,'utf-8')))[2:-1]}',"""
        keys = keys[:-1]
        values = values[:-1]
        querry = f"""INSERT INTO "{table}" ({keys}) VALUES({values})"""
        print(querry)
        cur.execute(querry)
        con.commit()
        con.close()
        return True

    def insert(self,table,dict_of):
        dico = dict_of
        f = Fernet(self.key)
        config = configparser.ConfigParser()
        config.read('config.ini')
        database = config["DATAS"]["database"]
        params = []
        for x in config["DATAS"]:
            y = bytes(config["DATAS"][x][2:],'utf-8')
            params.append(str(f.decrypt(y))[2:-1])
        con = psycopg2.connect(dbname = params[1],host = params[0],user = params[2],password = params[4])
        cur = con.cursor()
        keys = ""
        values = ""
        for i in dict_of.keys():
            keys = keys + f"""{i},"""
        for i in dict_of.values():
            if str(i).startswith("["):
                i = i.strip('][').split(',') 
                values = values + "["
                for y in range(len(i)) :
                    if y != len(i):
                            values = values + "'"+(i[y]) + "',"
                    else:
                        values = values + "'"+(i[y])
                values =  values + "],"
            else:
                values = values + f"""'{(i)}',"""
        keys = keys[:-1]
        values = values[:-1]
        querry = f"""INSERT INTO "{table}" ({keys}) VALUES({values})"""
        print(querry)
        cur.execute(querry)
        con.commit()
        con.close()
        return True


    def in_users(self,dico):
        dico = dico
        f = Fernet(self.key)
        config = configparser.ConfigParser()
        config.read('config.ini')
        database = config["DATAS"]["database"]
        database = bytes(database[2:len(database) - 1],'utf-8')
        params = []
        for x in config["DATAS"]:
            y = bytes(config["DATAS"][x][2:],'utf-8')
            params.append(str(f.decrypt(y))[2:-1])
        con = psycopg2.connect(dbname = params[1],host = params[0],user = params[2],password = params[4])
        cur = con.cursor()
        tuple_to_take = tuple(dico.keys())
        tupe_values = list(dico.values())
        tupe_values = tuple(tupe_values)
        querry = """SELECT"""
        for x in tuple_to_take:
            querry = querry + f""" "{x}","""
        
        querry = querry[:-1] + f""" FROM users"""
        cur.execute(querry)
        result = 0
        rows = cur.fetchall()
        tuple_to_take = tuple(i for i in rows)
        for x in tuple_to_take:
            for y in range(len(x)):
                truc = x[y]
                if str(f.decrypt(bytes(truc,'utf-8')))[2:-1] == tupe_values[y]:
                    result = result + 1
        
        if result == len(tupe_values):
            return True
        else:
            return False
    
    def select(self,table, list_name = "*",locate = "None"):
        """
        Penser à bien préciser le nom des paramètres
        select("[nom de la table]","[quelquechose]") n'est pas possible
        select("[nom de la table]",liste_name = "[quelquechose]",locate = "[quelquechose]")
        est la solution
        """
        f = Fernet(self.key)
        config = configparser.ConfigParser()
        config.read('config.ini')
        database = config["DATAS"]["database"]
        params = []
        for x in config["DATAS"]:
            y = bytes(config["DATAS"][x][2:],'utf-8')
            params.append(str(f.decrypt(y))[2:-1])
        con = psycopg2.connect(dbname = params[1],host = params[0],user = params[2],password = params[4])
        cur = con.cursor()
        if list_name == "*":
            if locate != "None":
                cur.execute(f"SELECT * from {table} WHERE {locate}")
                long = len(cur.description)
                rows = cur.fetchall()
                dico = []
                for r in rows:
                    dico.append([decrypted(str(r[i + 1])) for i in range(long - 1) if len(str(r[i + 1])) > 5])

                con.close()
            else:
                cur.execute(f"SELECT * from {table}")
                long = len(cur.description)
                rows = cur.fetchall()
                dico = []
                for r in rows:
                    dico.append([decrypted(str(r[i + 1])) for i in range(long - 1) if len(str(r[i + 1])) > 5])

                con.close()
        else:
            values = []
            for x in range(len(list_name)):
                liste = []
                if locate != "None":
                    cur.execute(f"""SELECT ({list_name[x]}) from {table} WHERE {locate};""")
                    descr = cur.description
                    rows = cur.fetchall()
                    for r in rows:
                        if len(str(r[0])) > 5:
                            liste.append(decrypted(str(r[0]))) 
                else:
                    cur.execute(f"""SELECT ({list_name[x]}) from {table};""")
                    descr = cur.description
                    rows = cur.fetchall()
                    for r in rows:
                        if len(str(r[0])) > 5:
                            liste.append(decrypted(str(r[0]))) 
                values.append(liste)
            dico = values
            con.close()
        return dico


def decrypted(word):
    f = Fernet(key)
    config = configparser.ConfigParser()
    config.read('config.ini')
    ariane = config["DATAS"]["ariane"]
    ariane = bytes(ariane[2:len(ariane) - 1],'utf-8')
    ariane = f.decrypt(ariane)
    fe = Fernet(ariane)
    if type(word) == list:
        for w in range(len(word)):
            w = bytes(w,'utf-8')
            word[w] = str(fe.decrypt(word[w]))[2:-1] #for prout
    else:
        word = bytes(str(word),'utf-8')
        word = str(fe.decrypt(word))[2:-1] #for other
    return word

def encrypted(word):
    key = getconf()
    f = Fernet(key)
    config = configparser.ConfigParser()
    config.read('config.ini')
    ariane = config["DATAS"]["ariane"]
    ariane = bytes(ariane[2:len(ariane) - 1],'utf-8')
    ariane = f.decrypt(ariane)
    fe = Fernet(ariane)
    if type(word) == list:
        for w in range(len(word)):
            w = bytes(w,'utf-8')
            word[w] = str(fe.encrypt(word[w]))[2:-1]
    else:
        word = bytes(word,'utf-8')
        word = str(fe.encrypt(word))[2:-1]

    return word


