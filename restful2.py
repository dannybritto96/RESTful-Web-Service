from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from json import dumps
from flask_jsonpify import jsonify
from flask_httpauth import HTTPBasicAuth
from Crypto.Cipher import XOR
import base64

db_connect = create_engine('sqlite:///EssentialSQL.db')
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
secret_key = 'Riverdale'

def decrypt(secret_key,ciphertext):
    cipher = XOR.new(secret_key)
    return cipher.decrypt(base64.b64decode(ciphertext))

@auth.verify_password
def verify(username,password):
    conn = db_connect.connect()
    try:
        query = conn.execute("select password from Users where username = \"{0}\"".format(username))
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        if decrypt(secret_key,result['data'][0]['password'].encode('ascii','ignore')) == password:
            return True
    except OperationalError as e:
        return False

class Customers(Resource):
    @auth.login_required
    def get(self,customer_id):
        conn = db_connect.connect()
        query = conn.execute("select * from Customers where CustomerID=%d;" % int(customer_id))
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    @auth.login_required
    def post(self):
        CompanyName = request.args.get('CompanyName')
        ContactName = request.args.get('ContactName')
        ContactTitle = request.args.get('ContactTitle')
        Address = request.args.get('Address')
        City = request.args.get('City')
        State = request.args.get('State')
        conn = db_connect.connect()
        try:
            query = conn.execute("insert into Customers(CompanyName,ContactName,ContactTitle,Address,City,State) values('{0}','{1}','{2}','{3}','{4}','{5}');".format(CompanyName,ContactName,ContactTitle,Address,City,State))
            return {'status':'success'}
        except:
            return {'status':'failed'}

    @auth.login_required
    def put(self):
        args = request.args
        params = {}
        customer_id = None
        update_query = "update Customers set "
        for i,j in args.iteritems():
            if i == 'CustomerID':
                customer_id = j
            update_query = update_query + "{0} = \"{1}\",".format(i,j)
        if customer_id == None:
            return {'status':'no primay key in passed parameter'}
            exit
        update_query = update_query[:-1]
        update_query = update_query + " where CustomerID = {};".format(customer_id)
        conn = db_connect.connect()
        try:
            query = conn.execute(update_query)
            query = conn.execute("select * from Customers where CustomerID=%d;" % int(customer_id))
            result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
            return jsonify(result)
        except:
            return {'status':'failed'}

    @auth.login_required
    def delete(self,customer_id):
        conn = db_connect.connect()
        try:
            query = conn.execute("delete from Customers where CustomerID=%d;" % int(customer_id))
            return {'status':'success'}
        except:
            return {'status':'failed'}

api.add_resource(Customers,'/api/customers',methods=['POST','PUT'],endpoint="customer")
api.add_resource(Customers,'/api/customers/<customer_id>',methods=['DELETE','GET'],endpoint="manage_customer")

if __name__ == '__main__':
    app.run(port='5002')
