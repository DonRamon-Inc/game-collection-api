import dotenv
import os

from app.app import iniciar_app

dotenv.load_dotenv()
app = iniciar_app()

port = os.getenv('PORT', 5000)
app.run(port=port)
