import csv, sqlite3
import xml.etree.ElementTree as ET
import os


def script():
    
    tree = ET.parse('dbpath.xml')
    root = tree.getroot()
    adress = tree.find('dbpath').text

    if not os.path.isfile(adress):

        con = sqlite3.connect(adress)
        cur = con.cursor()


        cur.execute("CREATE TABLE employees (id, name, position, countrycode);")
        cur.execute("CREATE TABLE countrycode (code, country);")



        #TABLE EMPLOYEES
        with open('employees.csv','rt') as fin: 
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['name'], i['position'], i['countrycode']) for i in dr]

        cur.executemany("INSERT INTO employees (id, name, position, countrycode) VALUES (?, ?, ?, ?);", to_db)



        #TABLE COUNTRYCODE
        with open('countries.csv','rt') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['code'], i['country']) for i in dr]

        cur.executemany("INSERT INTO countrycode (code, country) VALUES (?, ?);", to_db)



        con.commit()
        con.close()

    else:
        pass
