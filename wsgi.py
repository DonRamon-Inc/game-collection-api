import os
import dotenv

from .app.app import iniciar_app

dotenv.load_dotenv()
app = iniciar_app()

port = int(os.getenv('PORT', '5000'))
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
