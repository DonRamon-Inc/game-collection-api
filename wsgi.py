import dotenv

from app.app import iniciar_app

if __name__ == '__main__':
  dotenv.load_dotenv()
  app = iniciar_app()
  app.run(debug=True)
