import os
from flask import Flask

from views import politics_news
from models import db

# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db.init_app(app)

# register blueprints
app.register_blueprint(politics_news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
