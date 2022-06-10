import sqlalchemy as sa
from models.connection import conn
from models.utils import utils

table_user = sa.Table('user', sa.MetaData(),
  sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
  sa.Column('name', sa.String(255)),
  sa.Column('email', sa.String(255), unique=True),
  sa.Column('password', sa.String(255)),
  sa.Column('phone', sa.String(255)),
  sa.Column('level', sa.Integer)
)

class user():
  def single(id):
    query = table_user.select().where(table_user.c.id == id)
    result = conn.execute(query).fetchone()

    #convert to dict
    if result is not None:

      result = dict(result)
      #remove password, level, id
      del result['password']
      del result['level']
      del result['id']
      return result
    else:
      return False
    return result
  
  def get():
    query = table_user.select()
    result = conn.execute(query).fetchall()
    return result

  def insert(data):
    data['password'] = utils.hash(data['password'])
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

  def verify(email, password):
    password = utils.hash(password)
    query = table_user.select().where(table_user.c.email == email).where(table_user.c.password == password)
    result = conn.execute(query).fetchone()
    if result is not None:
      return result
    else:
      return False