import sqlalchemy as sa

DB_USER = 'root'
DB_PASS = ''
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'pifly'


conn = sa.create_engine(
  'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    db=DB_NAME
  )
)

table_user = sa.Table('user', sa.MetaData(),
  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
  sa.Column('name', sa.String(255)),
  sa.Column('email', sa.String(255)),
  sa.Column('password', sa.String(255)),
  sa.Column('phone', sa.String(255)),
  sa.Column('level', sa.Integer)
)

table_device = sa.Table('device', sa.MetaData(),
  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
  sa.Column('name', sa.String(255)),
  sa.Column('serial_number', sa.String(255)),
  sa.Column('battery', sa.Float),
  sa.Column('water', sa.Float),
  sa.Column('radar', sa.Float),
  sa.Column('interval', sa.Integer)
)

table_user_device = sa.Table('user_device', sa.MetaData(),
  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
  sa.Column('user_id', sa.Integer, sa.ForeignKey(table_user.c.id)),
  sa.Column('device_id', sa.Integer, sa.ForeignKey(table_device.c.id))
)

class user():
  def get(id):
    query = table_user.select().where(table_user.c.id == id)
    result = conn.execute(query).fetchone()
    return result
  
  def get():
    query = table_user.select()
    result = conn.execute(query).fetchall()
    return result

  def insert(data):
    query = table_user.insert().values(data)
    conn.execute(query)
    return True

  def update(data):
    query = table_user.update().where(table_user.c.id == data['id']).values(data)
    conn.execute(query)
    return True

  def delete(id):
    query = table_user.delete().where(table_user.c.id == id)
    conn.execute(query)
    return True

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