import os
import logging
from publisher import Publisher
from flask import Flask

from views import news

# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# register blueprints
app.register_blueprint(news)

if __name__ == '__main__':
    try:
        logging.info('Starting publisher connection')
        publisher = Publisher()
        publisher.start()
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        logging.info('Closing publisher connection')
        publisher.stop()
    except Exception as ex:
        logging.info('Interrrupted publisher connection')
        logging.error(str(ex))
        publisher.stop()
