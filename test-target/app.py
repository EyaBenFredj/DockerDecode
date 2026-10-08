import os

from flask import Flask

app = Flask(__name__)

# The secret is read when the container starts, never baked into the image.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.get("/")
def index():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"healthy": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)