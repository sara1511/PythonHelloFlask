from flask import Flask, request, jsonify
import pyodbc
import os
import jwt

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>It Works!</h1>"

@app.route('/token')
def token():
    my_id_token = request.headers['X-MS-TOKEN-AAD-ID-TOKEN']
    my_access_token = request.headers['X-MS-TOKEN-AAD-ACCESS-TOKEN']
    my_jwt_claims = jwt.decode(my_access_token, options={"verify_signature": False})
    my_jwt_header = jwt.get_unverified_header(my_access_token)
    my_access_token_expiry = request.headers['X-MS-TOKEN-AAD-EXPIRES-ON']
    # my_refresh_token = request.headers['X-MS-TOKEN-AAD-REFRESH-TOKEN']
    principal_name = request.headers['X-MS-CLIENT-PRINCIPAL-NAME']
    client_principal_id = request.headers['X-MS-CLIENT-PRINCIPAL-ID']
    return jsonify(
        access_token=my_access_token,
        expires_on=my_access_token_expiry,
        # refresh_token=my_refresh_token,
        id_token=my_id_token,
        email_id=principal_name,
        user_id=client_principal_id,
        jwt_header=my_jwt_header,
        jwt_claims=my_jwt_claims
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