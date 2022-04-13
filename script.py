import csv, sqlite3
import xml.etree.ElementTree as ET

tree = ET.parse('dbpath.xml')
root = tree.getroot()
adress = tree.find('dbpath').text

con = sqlite3.connect(adress)
cur = con.cursor()

cur.execute("CREATE TABLE employees (id, name, position, contrycode);")
cur.execute("CREATE TABLE countrycode (code, country);")

con.commit()
con.close()