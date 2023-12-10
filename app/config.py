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

GATEWAY_IP = os.environ.get("GATEWAY_IP")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_DOMAIN_NAME = os.environ.get("ADMIN_DOMAIN_NAME")
DOMAIN_ID = os.environ.get("DOMAIN_ID")
ADMIN_PROJECT_NAME = os.environ.get("ADMIN_PROJECT_NAME")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_ID = os.environ.get("ADMIN_ID")

READER = os.environ.get("READER")
ADMIN = os.environ.get("ADMIN")
MEMBER = os.environ.get("MEMBER")
IP_VERSION = os.environ.get("IP_VERSION")
CIDR = os.environ.get("CIDR")