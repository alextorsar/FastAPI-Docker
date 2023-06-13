import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_url: str = os.getenv('URL_MONGO')
    db_user: str = os.getenv('USER')
    db_pass: str = os.getenv('PASSWORD')
    db_host: str = os.getenv('HOST')
    db_port: str = os.getenv('PORT')
    salt: str = os.getenv('SALT')
