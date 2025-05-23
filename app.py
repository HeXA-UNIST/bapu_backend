from src.middleware import create_app
from config import config

from src.service import api

app = create_app(config)
app.register_blueprint(api)


@app.route("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
