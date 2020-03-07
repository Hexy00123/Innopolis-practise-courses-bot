from config import DB as db
from model import *

db.connect()
db.create_tables([User, Message])
db.close()
