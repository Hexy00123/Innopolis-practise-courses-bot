import peewee
import config


class BaseModel(peewee.Model):
    class Meta:
        database = config.DB


class User(BaseModel):  # содержит в себе tg_id юзера и его имя
    tg_id = peewee.BigIntegerField()
    full_name = peewee.CharField()


class Message(BaseModel):  # содержит в себе id сообщения, id чата, текст сооб, id отправителя
    message_id = peewee.BigIntegerField()
    chat_id = peewee.BigIntegerField()
    text = peewee.TextField()
    tg_id = peewee.BigIntegerField()
    user = peewee.ForeignKeyField(User, backref='messages')
