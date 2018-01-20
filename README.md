# python-simple-http-logger
Простой логгер с доступом по http

## Запуск

В автоматическом режиме
`sh run.sh`

В ручном режиме:
* Запуск сервера логгера
```
mkdir logs
python3 server.py
```
* Запуск простого web клиента
```
cd logs
python3 -m http.server 9001
```
