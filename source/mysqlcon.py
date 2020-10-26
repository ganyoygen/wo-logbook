import os
import mysql.connector
from configparser import ConfigParser
from tkinter import messagebox

getfile = str(os.getcwd())+"\\"+"config.ini"

def read_db_config(filename=getfile, section='mysql'):
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
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def getdata_all(opsi,data):
    try:
        db_config = read_db_config()
        con = mysql.connector.connect(**db_config)
        cur = con.cursor()
        cur.execute(opsi, data)
        results = cur.fetchall()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", \
            message="SQL Log: {}".format(err))
    finally:
        if (con.is_connected()):
            cur.close()
            con.close()

def getdata_one(opsi,data):
    try:
        db_config = read_db_config()
        con = mysql.connector.connect(**db_config)
        cur = con.cursor()
        cur.execute(opsi, data)
        results = cur.fetchone()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", \
            message="SQL Log: {}".format(err))
    finally:
        if (con.is_connected()):
            cur.close()
            con.close()