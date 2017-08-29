import os

log_config = {

    'version' : 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(threadName)s][%(filename)s][%(lineno)d][%(levelname)s]: %(message)s'
        }
    },

    'handlers': {
        'default' : {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': os.path.join(os.path.dirname(__file__), './logs/scraper.log')
         },
    },

    'loggers' : {
        'scraper': {
            'handlers': ['default'],
            'level': 'INFO',
            'propogate': False
        }
    },
    'disable_existing_loggers': True
}