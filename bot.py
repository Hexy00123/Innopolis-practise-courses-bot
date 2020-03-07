import model
import peewee
import config
import logging
import datetime as dt
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # если что-то не робит, то эта часть кода в консоль пишет что за ошибка
logger = logging.getLogger(__name__)


def save(update, context):
    msg: telegram.Message = update.message  # достаем сообщение
    user, created = model.User.get_or_create(tg_id=msg.from_user.id, defaults={
        'full_name': msg.from_user.full_name})  # метод создает нового юзера, если его нету и сздает его tg_id
    data = {  # словарь значений(чтобы каждый раз значение не прописывать)
        'message_id': msg.message_id,
        'chat_id': msg.chat_id,
        'text': msg.text,
        'tg_id': msg.from_user.id,
        "user": user.id
    }
    model.Message.create(**data)  # append to DB


def last(update, context):
    last = 1
    if len(context.args) > 0:
        last = int(context.args[0])
    msg: telegram.Message = update.message
    for msg2 in model.Message.filter(chat_id=msg.chat_id).order_by(model.Message.id.desc()).limit(last):
        msg.reply_text(f'User:{msg2.user.full_name} \n wrote: {msg2.text}')

# эта функция выполняется, когда пишется /start посмотри это ниже, там эта f() и используется
def start(update, context):
    update.message.reply_text('Hi!')


# эта функция выполняется, когда пишется /help посмотри это ниже, там эта f() и используется
def help(update, context):
    update.message.reply_text('Help!')


# работает только в том случае, если что-то сломалось
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # создает бота с токеном config.TOKEN, 2 аргумент пока что важен
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher  # cоздание менеджера хэндлеров
    # handlers, вызывают f(), если кто-то пишет команды/сообщения
    dp.add_handler(CommandHandler("start", start))  # вызывет start(), если нам написали /start
    dp.add_handler(CommandHandler("help", help))  # вызывет start(), если нам написали /start
    dp.add_handler(CommandHandler('last', last))
    dp.add_handler(MessageHandler(Filters.text, save))

    dp.add_error_handler(error)  # если ошибка, то вызывает error()

    # Start the Bot
    if config.HEROKU_APP_NAME is None:
        updater.start_polling()  # врубает бота с локалки

    else:
        updater.start_webhook(listen='0.0.0.0', port=config.PORT, url_path=config.TOKEN, )
        updater.bot.set_webhook(
            f'https://{config.HEROKU_APP_NAME}.herokuapp.com/{config.TOKEN}')  # врубает бота с сервера
    updater.idle()  # ==while True


if __name__ == '__main__':
    main()
