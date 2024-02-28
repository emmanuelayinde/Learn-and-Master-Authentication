from flask import Flask, request, jsonify, make_response, session, render_template
from datetime import datetime, timedelta
from functools import wraps
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c5636ae570b54beb82c27e1ee5a8ff0d'


user = { 
    'password': 'password'
}

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request / args.get('token')
        if not token:
            return jsonify({"Alert": "Token is missing"})
        
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
             return jsonify({"Alert": "Invalid token"})
    return decorated        
    

@app.route("/")
def home():
    if not session.get('is_logged_in'):
        return render_template('login.html')
    else:
        return "Logged in currently"

@app.route('/public')
def public():
   return "For public"

@app.route("/auth")
@token_required
def auth():
    return "JWT verifield, welcome home"

@app.route("/login", methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == user['password']:
        session["is_logged_in"] = True
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        },
        app.config['SECRET_KEY'])
        return jsonify({'user_token': token.decode('utf-8')})

    else:
        return make_response("Unable to very", 403, {'WWW-Authenticate': 'Basic realm: Authentication failed!'})



if __name__ == "__main__":
    app.run(debug=True)
