import os
import logging
from subscriber import Subscriber
from flask import Flask

from views import recommendation

# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# register blueprints
app.register_blueprint(recommendation)

subscriber = None

if __name__ == '__main__':
    try:
        logging.info('Starting subscriber connection')
        subscriber = Subscriber()
        subscriber.start()
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        logging.info('Closing subscriber connection')
        subscriber.close()
    except Exception as ex:
        logging.info('Interrrupted subscriber connection')
        logging.error(str(ex))
        subscriber.close()
