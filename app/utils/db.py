from app.utils.settings import Settings

settings = Settings()

HOST = settings.db_host
PORT = int(settings.db_port)
USER = settings.db_user
PASSWORD = settings.db_pass

URL_MONGO = settings.db_url

SALT = b'Lur9vFWtHdexGGUsYbe7Tni0zjvSVvC0gt3Tm4RebKM='