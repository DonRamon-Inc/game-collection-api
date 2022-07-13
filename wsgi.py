import dotenv

from app.app import iniciar_app

dotenv.load_dotenv()
app = iniciar_app()
app.run()
