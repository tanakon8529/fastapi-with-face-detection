import os
from dotenv import load_dotenv

load_dotenv("./.env")

API_VERSION = os.environ["API_VERSION"]
API_PATH = os.environ["API_PATH"]
API_DOC = os.environ["API_DOC"]
SERVER_ROLE = os.environ["SERVER_ROLE"]
JWT_PUBLIC_KEY = os.environ["JWT_PUBLIC_KEY"]
ACCESSTOKEN_FILE_PATH = os.environ["ACCESSTOKEN_FILE_PATH"]

FIRST_DEVUSER = os.environ["FIRST_DEVUSER"]
FIRST_DEVUSER_PASSWORD = os.environ["FIRST_DEVUSER_PASSWORD"]

