from peewee import SqliteDatabase  # эта библиотека для создания и работы с БД
from decouple import config
from playhouse.db_url import connect

TOKEN = config('TOKEN')
DB = connect(config('DB_URL', default='sqlite:///bot.db'))  # сама БДшка
PORT = config('PORT', default=8443)
HEROKU_APP_NAME = config('HEROKU_APP_NAME', default=None)
