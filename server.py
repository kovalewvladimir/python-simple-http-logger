"""
vek 18.01.2018

Отправить запрос:
    1. Через bash:
        curl --data 't=Текст лога \r\n - Перенос строки' http://хост:порт/имя_папка/имя_файла.log
    2. Через PowerShell:
        Invoke-WebRequest -Uri "http://хост:порт/имя_папка/имя_файла.log" -Method Post -Body @{"t"= "Текст лога \r\n - Перенос строки"}
"""

import time
import sys
import os
import cgi
import logging
import logging.config
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 9000
REAL_PATH = os.path.realpath(os.path.dirname(sys.argv[0]))

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        response_ok    = bytes('Ок', 'UTF-8')
        response_error = bytes('Error', 'UTF-8')

        text = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        text = text.getvalue('t')
        text = text.replace('\\r\\n', '\r\n')

        log_file = REAL_PATH + '/logs' + self.path
        log_dir  = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        if os.path.exists(log_file):
            f = open(log_file, 'a')
        else:
            f = open(log_file, 'w')

        f.write('-'*100 + '\r\n')
        f.write('-'*40 + datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") + '-'*41 + '\r\n')
        f.write('-'*100 + '\r\n\r\n')
        f.write(text + '\r\n\r\n')
        f.close()

        self.wfile.write(response_ok)

        
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':

    # Логирование
    logConfig = {
        "version":1,
        "handlers":{
            "fileHandler":{
                "class":"logging.FileHandler",
                "formatter":"verbose",
                "filename":"server.log",
            },
            "consoleHandler":{
            "class": "logging.StreamHandler",
            "formatter": "verbose"
            },
        },
        "loggers":{
            "server":{
                "handlers":["fileHandler", "consoleHandler"],
                "level":"INFO",
            }
        },
        "formatters":{
            "verbose":{
                "format":"%(asctime)s - %(levelname)s - %(message)s"
            }
        }
    }
    logging.config.dictConfig(logConfig)
    logger = logging.getLogger("server")


    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    logger.info('Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info('Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
