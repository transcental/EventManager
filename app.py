from utils.slack import app
from utils.env import env

if __name__ == "__main__":
    app.start(env.port)