import sqlalchemy as sa
from models.connection import conn

table_device = sa.Table('device', sa.MetaData(),
  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
  sa.Column('name', sa.String(255)),
  sa.Column('serial_number', sa.String(255)),
  sa.Column('battery', sa.Float),
  sa.Column('water', sa.Float),
  sa.Column('radar', sa.Float),
  sa.Column('interval', sa.Integer)
)

class device():
  def get(id):
    query = table_device.select().where(table_device.c.id == id)
    result = conn.execute(query).fetchone()
    return result
  
  def get():
    query = table_device.select()
    result = conn.execute(query).fetchall()
    return result
  
  def insert(data):
    query = table_device.insert().values(data)
    conn.execute(query)
    return True
  
  def update(data):
    query = table_device.update().where(table_device.c.id == data['id']).values(data)
    conn.execute(query)
    return True
  
  def delete(id):
    query = table_device.delete().where(table_device.c.id == id)
    conn.execute(query)
    return True
