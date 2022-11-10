from flask import Flask
app = Flask(__name__)
app.secret_key = 'this will be an ENV variable'