<h2 align="center"> Python CRUD API </h2>

CRUD API in python3 using **Flask**

Routes tested with **Postman**

Create database, tables and import csv files with **python script**

**SQLite3** database with two tables (using join)

*Libs:*
* sqlite3
* csv
* os
* ElementTree
* request
* jsonify

*Steps:*
* Download the repository.
* Change the 'dbpath.xml' file with the address where you want the database to be saved.
* Run API.

When the API is started, it checks if the database exists at the address entered in dbpath.xml, if it does not have a database with the chosen name, it executes a script found in the script.py file.
It will create the database, tables and import information from CSV files into these tables.
Thus creating the complete database.
