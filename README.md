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


## logging

```
from logging.handlers import HTTPHandler
import logging


class LogHttpHandler(HTTPHandler):

    def mapLogRecord(self, record):
        """
        Map log record as required format of HTTP/HTTPS server
        :param record:
        :return:
        """
        record_modified = HTTPHandler.mapLogRecord(self, record)
        record_modified['t'] = record_modified['msg'].encode('utf-8')
        return record_modified


logger = logging.getLogger("test")
logger.setLevel(logging.INFO)

_logger = LogHttpHandler('192.1.13.16:9000', '/py/123.txt', 'POST', False)
_logger.setLevel(logging.INFO)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# _logger.setFormatter(formatter)

logger.addHandler(_logger)

logger.info("123123123")
```
