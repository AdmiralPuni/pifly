import sqlalchemy as sa
from models.connection import conn
from models.user import table_user
from models.device import table_device

table_user_device = sa.Table('user_device', sa.MetaData(),
  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
  sa.Column('user_id', sa.Integer, sa.ForeignKey(table_user.c.id)),
  sa.Column('device_id', sa.Integer, sa.ForeignKey(table_device.c.id))
)

class user_device():
  def get_user_device(user_id):
    query = table_user_device.select().where(table_user_device.c.user_id == user_id)
    result = conn.execute(query).fetchall()
    return result
  
  def insert(data):
    query = table_user_device.insert().values(data)
    conn.execute(query)
    return True
  
  def update(data):
    query = table_user_device.update().where(table_user_device.c.id == data['id']).values(data)
    conn.execute(query)
    return True
  
  def delete(id):
    query = table_user_device.delete().where(table_user_device.c.id == id)
    conn.execute(query)
    return True