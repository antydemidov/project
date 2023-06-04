import os

import dotenv

from app import app

if __name__ == '__main__':
    dotenv.load_dotenv()
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    PORT = int(os.environ.get('SERVER_PORT', 5000))

    app.run(HOST, PORT)
