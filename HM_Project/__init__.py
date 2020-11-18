"""
The flask application package.
"""

from flask import Flask
from flask_restful import Api,Resource
from .resource.registration import Registration
from HM_Project.database import DataBase
from HM_Project.config import postgresqlConfig

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig

@app.route('/')
def getname():
   return "Hello"

api = Api(app)

@app.before_first_request
def create_tables():
  
     DataBase.CreateTable()

@app.route('/register', methods = ['POST'])
def registration_fun() :
    registerinstance = Registration()
    return registerinstance.insert_Customerdata()