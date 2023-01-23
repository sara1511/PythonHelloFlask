from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>It Works Team!!</h1>"

@app.route('/token')
def token():
    myidtoken = request.headers['X-MS-TOKEN-AAD-ID-TOKEN']
    myaccesstoken = request.headers['X-MS-TOKEN-AAD-ACCESS-TOKEN']
    myaccesstokenexpiry = request.headers['X-MS-TOKEN-AAD-EXPIRES-ON']
    myrefreshtoken = request.headers['X-MS-TOKEN-AAD-REFRESH-TOKEN']
    return jsonify(
        access_token=myaccesstoken,
        expires_on=myaccesstokenexpiry,
        refresh_token=myrefreshtoken,
        id_token=myidtoken
    )

@app.route('/sql')
def sql():
    server = 'tcp:' + os.environ['DB_HOST'] + ',' + os.environ['DB_PORT']
    database = os.environ['DB_NAME']
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password+';TrustServerCertificate=yes')
    cursor = cnxn.cursor()

    #Sample select query
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone() 
    sqlversion = ""
    while row: 
        sqlversion = (row[0])
        row = cursor.fetchone()
    return sqlversion

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = '8081')