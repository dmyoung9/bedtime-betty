from dotenv import load_dotenv

from betty.app import quart_app

load_dotenv()

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True


if __name__ == "__main__":
    quart_app.run(host=HOST, port=PORT, debug=DEBUG)
