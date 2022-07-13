import dotenv
import os

from app.app import iniciar_app

dotenv.load_dotenv()
app = iniciar_app()

port = int(os.getenv('PORT', 5000))
app.run(host="0.0.0.0", port=port)
