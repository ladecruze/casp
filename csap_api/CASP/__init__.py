import secrets, os, psycopg2, hashlib, json
from flask import abort, render_template, request, Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)

import CASP.API_vulnerabilities.BOLA.Exploiting_IDOR_vulnerability.app
import CASP.API_vulnerabilities.Broken_User_Authentication.jwt
import CASP.what_is_api.learn_the_basics_of_curl.learn_curl
import CASP.init_db

def getConnection():
    conn = psycopg2.connect(host='casp-db-1',
                            database='casp',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

swagger = Swagger(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

'''@app.route('/mongo', methods=['GET'])  
def get_data():
    """Returns a list of todo item
    ---
    produces:
    - ""
    responses:
      200:
        description: "list of tasks"
      400:
        description: "Invalid ID supplied"
      404:
        description: "todo item not found"
    """
    items = dbcoll.find_one({"id":"U1IT00003"})
    return json.dumps(items, default=str)
'''

#registration with mass assignment vulnerability
@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    """Register a new user
    ---
    post:
        produces:
        - "application/json"
        responses:
          200:
            description: "User has been added"

          400:
            description: "Invalid ID supplied"
          404:
            description: "todo item not found"
    get:
        produces:
        - "text/html"
        responses:
          200:
            description: "Login page"

          400:
            description: "Invalid ID supplied"
          404:
            description: "todo item not found"
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = hashlib.md5(request.args.get('password')).hexdigest()
        role = request.args.get('role')
        secret = secrets.token_urlsafe(32)
        conn = getConnection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users;')
        if(role is not None):
            cur.execute('INSERT INTO users (name, email, role, password, key) VALUES (%s, %s, %s, %s, %s)',(username, email, role, password, secret))
        else:
            cur.execute('INSERT INTO users (name, email, role, password, key) VALUES (%s, %s, %s, %s, %s)',(username, email, 'user',password, secret))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message='registered successfully',apikey=secret)
    if request.method == 'GET':
        return render_template('register.html')

@app.route('/key', methods=['GET', 'POST'])  
def get_api_key():
    """Log in to get API key
    ---
    produces:
    - "application/json"
    responses:
      200:
        description: ""
      400:
        description: "Invalid ID supplied"
      404:
        description: "todo item not found"
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.md5(request.form.get('password').encode('utf8')).hexdigest()
        print(password)
        conn = getConnection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email=%(email)s',{"email":email})
        users = cur.fetchall()
        print(users)
        cur.close()
        conn.close()
        try:
            if(users[0][2] == email and users[0][3] == password):
                return render_template('documentation.html',apikey=users[0][5])
            else:
                return abort(403)
        except IndexError:
            return "user not available"
    if request.method == 'GET':
        return render_template('login.html')
