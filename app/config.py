import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://')
SECRET_KEY = os.getenv('SECRET_KEY')
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
STEAM_API_URL = os.getenv('STEAM_API_URL')
