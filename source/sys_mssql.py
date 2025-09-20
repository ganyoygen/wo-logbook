import os
# pip install pypyodbc
import pypyodbc
from configparser import ConfigParser
from tkinter import messagebox
from sys_pwhash import decode

getfile = str(os.getcwd())+"\\"+"config.ini"

def read_db_config_ms(filename=getfile, section='mssql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            if item[0] == 'pwd':
                db[item[0]] = decode(item[1])
            else: db[item[0]] = item[1]

        if db['cek'] != '1': 
            # print('mssql tidak aktif')
            db = {}
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    return db

def mssql_all(query,param):
    try:
        con = pypyodbc.connect(**read_db_config_ms())
        cur = con.cursor()
        cur.execute(query, param)
        results = cur.fetchall()
        cur.close()
        con.close()
        return results
    except pypyodbc.Error as err:
        messagebox.showerror(title="Error", \
            message="SQL Log: {}".format(err))

def mssql_one(query):
    try:
        con = pypyodbc.connect(**read_db_config_ms())
        cur = con.cursor()
        cur.execute(query)
        results = cur.fetchone()
        cur.close()
        con.close()
        return results
    except pypyodbc.Error as err:
        messagebox.showerror(title="Error", \
            message="SQL Log: {}".format(err))

def insert_mssql(query,param):
    try:
        con = pypyodbc.connect(**read_db_config_ms())
        cur = con.cursor()
        cur.execute(query, param)
        con.commit()
        cur.close()
        con.close()
        return True
    except pypyodbc.Error as err:
        messagebox.showerror(title="Error", \
            message="SQL Log: {}".format(err))