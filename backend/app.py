from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB

mysql = MySQL(app)
CORS(app)

from routes.applicant import applicant_bp
from routes.center import center_bp
app.register_blueprint(applicant_bp, url_prefix='/api/applicant')
app.register_blueprint(center_bp, url_prefix='/api/center')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
