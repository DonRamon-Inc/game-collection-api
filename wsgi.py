import dotenv
import os

from app.app import iniciar_app

dotenv.load_dotenv()
app = iniciar_app()

port = int(os.getenv('PORT', 5000))
if __name__ == '__main__':
  dotenv.load_dotenv()
  app = iniciar_app()
  app.run()
