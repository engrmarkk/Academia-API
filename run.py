from api import create_app
from api.config import config_object


app = create_app(configure=config_object['prodcon'])

if __name__ == "__main__":
    app.run(debug=True)
