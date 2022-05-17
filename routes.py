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

    result = cur.execute('''
    SELECT employees.id, employees.name, employees.position, countrycode.country
    FROM employees INNER JOIN countrycode ON employees.countrycode = countrycode.code;''') 
    
    retorno = []
    for row in result.fetchall():
        item = {}
        item['id'] = row['id']
        item['name'] = row['name']
        item['position'] = row['position']
        item['country'] = row['country']
        retorno.append(item)

    return jsonify(retorno)


#GET (INDIVIDUAL)

@app.route("/employees/id") 
def companyEmployee():

    body = request.get_json()

    tree = ET.parse('dbpath.xml')
    root = tree.getroot()
    adress = tree.find('dbpath').text

    conn = sqlite3.connect(adress)
    cur = conn.cursor()

    result = cur.execute('''
    SELECT employees.id, employees.name, employees.position, countrycode.country
    FROM employees, countrycode
    WHERE employees.countrycode = countrycode.code AND id = '{0}';
    '''.format(body["id"]))

    return jsonify(result.fetchall())


#POST

@app.route("/employees/add", methods=["POST"])
def addEmployee():

    body = request.get_json()

    if("id" not in body):
        return generateResponse(400, "The 'id' parameter is required!")
    if ("name" not in body):
        return generateResponse(400, "The 'name' parameter is required!")
    if ("position" not in body):
        return generateResponse(400, "The 'position' parameter is required!")
    if ("countrycode" not in body):
        return generateResponse(400, "The 'countrycode' parameter is required!")

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

    return generateResponse(200, "Employee Added!", "name:", body["name"])


#PUT

@app.route("/employees/update", methods=["PUT"])
def updateEmployee():

    body = request.get_json()

    tree = ET.parse('dbpath.xml')
    root = tree.getroot()
    adress = tree.find('dbpath').text

    conn = sqlite3.connect(adress)
    cur = conn.cursor()

    if ("id" not in body):
        return generateResponse(400, "The 'id' parameter is required!")
    else:
        name = 'NULL'
        position = 'NULL'
        countrycode = 'NULL'

        if ("name" in body):
            name = "'{}'".format(body["name"])
        if ("position" in body):
            position = "'{}'".format(body["position"])
        if ("countrycode" in body):
            countrycode = "'{}'".format(body["countrycode"])

        result = cur.execute('''
        UPDATE
          employees
        SET
          name = coalesce({0}, name), 
          position = coalesce({1}, position), 
          countrycode = coalesce({2}, countrycode)        
        WHERE id = '{3}';
        '''.format(name, position, countrycode, body["id"]))

    conn.commit()
    conn.close()

    return generateResponse(200, "Employee Updated", "name:", body["name"])


#DELETE

@app.route("/employees/delete", methods=["DELETE"]) 
def deleteEmployee():

    body = request.get_json()

    if ("id" not in body):
        return generateResponse(400, "Only inform the 'id' parameter")

    tree = ET.parse('dbpath.xml')
    root = tree.getroot()
    adress = tree.find('dbpath').text

    conn = sqlite3.connect(adress)
    cur = conn.cursor()

    result = cur.execute("DELETE from employees WHERE id = '{0}';".format(body["id"]))

    conn.commit()
    conn.close()

    return generateResponse(200, "Employee Deleted", "id:", body["id"])

#RESPONSES

def generateResponse(status, message, content_name=False, content=False):
    response = {}
    response["status"] = status
    response["message"] = message

    if(content_name and content):
        response[content_name] = content

    return response


app.run()