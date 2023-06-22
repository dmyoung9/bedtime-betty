from betty import quart_app

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True


if __name__ == "__main__":
    quart_app.run(host=HOST, port=PORT, debug=DEBUG)
