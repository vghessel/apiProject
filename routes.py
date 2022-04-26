from flask import Flask, request, jsonify
import sqlite3
import xml.etree.ElementTree as ET

app = Flask("main")


#GET

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


#GET INDIVIDUAL

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


<<<<<<< HEAD
#POST

@app.route("/employees/add", methods=["POST"])
def addEmployee():

    body = request.get_json()

    if("id" not in body):
        return generateResponse(400, "The id parameter is required!")
    if ("name" not in body):
        return generateResponse(400, "The name parameter is required!")
    if ("position" not in body):
        return generateResponse(400, "The position parameter is required!")
    if ("countrycode" not in body):
        return generateResponse(400, "The countrycode parameter is required!")

    tree = ET.parse('dbpath.xml')
    root = tree.getroot()
    adress = tree.find('dbpath').text

    conn = sqlite3.connect(adress)
    cur = conn.cursor()

    result = cur.execute('''
    INSERT INTO 
        employees (id, name, position, countrycode) 
    VALUES ('{0}', '{1}', '{2}', '{3}');
    '''.format(body["id"], body["name"], body["position"], body["countrycode"]))

    conn.commit()
    conn.close()

    return generateResponse(200, "Added employee!", "name:", body["name"])


#PUT


#DELETE


#RESPONSES

def generateResponse(status, message, content_name=False, content=False):
    response = {}
    response["status"] = status
    response["message"] = message

    if(content_name and content):
        response[content_name] = content

    return response


app.run()
=======
app.run()
>>>>>>> 2a38d304bcfccdec8d66db3e9f51e4f3a4bc19cb
