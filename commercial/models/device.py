import sqlalchemy as sa
from models.connection import conn
from models.user import table_user

table_device = sa.Table('device', sa.MetaData(),
  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
  sa.Column('user_id', sa.Integer, sa.ForeignKey(table_user.c.id)),
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

  def get_experiment():
    EXPERIMENT_USER_EMAIL = 'exp@mail.com'
    query = table_user.select().where(table_user.c.email == EXPERIMENT_USER_EMAIL)
    user_id = conn.execute(query).fetchone()['id']
    query = table_device.select().where(table_device.c.user_id == user_id)
    result = conn.execute(query).fetchall()
    return result

  def get_test_by_email(email):
    query = table_user.select().where(table_user.c.email == email)
    user_id = conn.execute(query).fetchone()['id']
    query = table_device.select().where(table_device.c.user_id == user_id)
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

  def update_by_serial_number(data):
    query = table_device.update().where(table_device.c.serial_number == data['serial_number']).values(data)
    conn.execute(query)
    return True

  def get_interval_by_serial_number(serial_number):
    query = table_device.select().where(table_device.c.serial_number == serial_number)
    result = conn.execute(query).fetchone()
    if result:
      return result['interval']
    else:
      return False
  
  def delete(serial_number, user_id):
    #verify if the device is owned by the user
    query = table_device.select().where(table_device.c.serial_number == serial_number).where(table_device.c.user_id == user_id)
    result = conn.execute(query).fetchone()
    if result:
      query = table_device.delete().where(table_device.c.serial_number == serial_number).where(table_device.c.user_id == user_id)
      conn.execute(query)
      return True
    
    return False

  def user_devices(user_id):
    query = table_device.select().where(table_device.c.user_id == user_id)
    result = conn.execute(query).fetchall()
    #convert to dict
    devices = []
    for row in result:
      device = {
        'id': row['id'],
        'name': row['name'],
        'serial_number': row['serial_number'],
        'battery': row['battery'],
        'water': row['water'],
        'radar': row['radar'],
        'interval': row['interval']
      }
      devices.append(device)
    return devices
