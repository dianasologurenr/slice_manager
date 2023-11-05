from dotenv import load_dotenv
import os

# Carga de variables de entorno
load_dotenv()

# Variables de entorno
SERVER = os.environ.get("HEADNODE_SERVER")
PORT = os.environ.get("HEADNODE_PORT")

ALGORITHM = os.environ['ALGORITHM']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY'] 
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']

SQLALCHEMY_DATABASE_URL = os.environ['SQLALCHEMY_DATABASE_URL']