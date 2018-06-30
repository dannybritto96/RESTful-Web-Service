# RESTful Web Service using Python Flask
A basic restful web service built using Flask for inserting, viewing, updating and deleting fields in a SQLite database.


## Requirements
All the requirements are listed in requirements.txt file.

```pip install -r requirements.txt```

## Requests

* GET - To fetch individual record
* POST - To add new record
* PUT - To edit existing record
* DELETE - To delete existing record

## Authentication

Authentication is done using Flask-HTTPAuth. Passwords are encrypted in the database.
Default user credentials are username=admin and password=password.

## Usage
```
import requests
import json
s = requests.Session()
s.auth = ('admin','password')

# GET record of Customer where CustomerId = 4
r = s.get('http://127.0.0.1:5002/api/customers/4')
print r.json()

# POST new record
data = {'CompanyName':'ABC','ContactName':'John Doe','ContactTitle':'Mr','Address':'123, Street','City':'Chennai','State':'Tamilnadu'}
r = s.post("http://127.0.0.1:5002/api/customers",params=data)
print r.json()

# PUT Update an exisiting record
data = {'CompanyName':'XYZ','CustomerID':12}
r = s.put("http://127.0.0.1:5002/api/customers",params=data)
print r.json()

# DELETE an exisiting record (CustomerId = 12)
r = s.delete("http://127.0.0.1:5002/api/customers/12")
```

## To encrypt password

```
from Crypto.Cipher import XOR
import base64
key = 'Riverdale'
def encrypt(key, plaintext):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))
  
ciphertext = encrypt(key,'password')
print ciphertext
```

Thank you essentialSQL for the sample database. 
https://www.essentialsql.com/get-ready-to-learn-sql-how-to-install-sqlite-and-the-sample-database/


