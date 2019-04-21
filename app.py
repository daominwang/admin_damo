from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 注册蓝图
from view import view

app.register_blueprint(view)

from model.user import *

if __name__ == '__main__':
    app.run(debug=True, port=8888)
