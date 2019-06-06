# python-simple-http-logger
Простой логгер с доступом по http

## Запуск

```
mkdir -p /docker/httplogger
cd /docker/httplogger
wget https://raw.githubusercontent.com/kovalewvladimir/python-simple-http-logger/master/docker-compose.yml
touch server.log
docker-compose up -d
```


## example_logging.py

```python
import logging.config
import os
from datetime import datetime

log_file_name = '%s.log' % datetime.now().strftime('%Y.%m.%d_%H_%M')
log_file_path = os.path.join(os.getcwd(), 'log', log_file_name)

os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

log_config = {
    'version': 1,
    'handlers': {
        'fileHandler': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': log_file_path,
        },
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'httpHandler': {
            'class': 'SimpleHttpHandler.SimpleHttpHandler',
            'host': '127.0.0.1:9000',
            'url': '/py/123.txt',
            'method': 'POST',
            'secure': False,
            'no_date': 'true',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'default': {
            'handlers': ['fileHandler', 'consoleHandler', 'httpHandler'],
            'level': 'INFO',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s\t%(levelname)s:\t%(message)s'
        }
    }
}

logging.config.dictConfig(log_config)
logger = logging.getLogger('default')

logger.info('test')
logger.error('error')
```
