from flask import Flask, request, jsonify
import sqlite3
import xml.etree.ElementTree as ET


app = Flask("main")


@app.route("/employees", methods=["GET"])   
def companyEmployees():

    tree = ET.parse('dbpath.xml')
    root = tree.getroot()
    adress = tree.find('dbpath').text

    conn = sqlite3.connect(adress)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    result = cur.execute("SELECT * from employees;")
    
    retorno = []
    for row in result.fetchall():
        item = {}
        item['id'] = row['id']
        item['name'] = row['name']
        item['position'] = row['position']
        item['countrycode'] = row['countrycode']
        retorno.append(item)

    return jsonify(retorno)



@app.route("/employees/id")    
def companyEmployee():

    body = request.get_json()

    tree = ET.parse('dbpath.xml')
    root = tree.getroot()
    adress = tree.find('dbpath').text

    conn = sqlite3.connect(adress)
    cur = conn.cursor()

    result = cur.execute("SELECT * from employees WHERE id = '{0}';".format(body["id"]))

    return jsonify(result.fetchall())


app.run()
