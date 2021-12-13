from peewee import *
from playhouse.sqlite_ext import JSONField
from pony.orm import select

db = SqliteDatabase('orders.db')


class OrderConfirmed(Model):
    size = CharField()
    pay = CharField()
    user_id = IntegerField()

    class Meta:
        database = db

class UserState(Model):

    user_id = IntegerField(unique=True)
    scenario_name = CharField()
    step_name = CharField()
    context = JSONField()
    class Meta:
        database = db


db.connect()
with db:
    db.create_tables([UserState, OrderConfirmed])
    # db.generate_mapping(create_tables=True)

# UserState.drop_table(with_all_data=True)
# OrderConfirmed.drop_table(with_all_data=True)


# with db:
#     select(s for s in UserState if s.user_id > 0)[:].show()
#     select(s for s in OrderConfirmed if s.user_id > 0)[:].show()
