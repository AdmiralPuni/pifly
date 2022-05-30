import sqlalchemy as sa

DB_USER = 'mg_pifly'
DB_PASS = 'UsadaPekora'
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

def main():
  #create all table
  table_user.create(conn)
  table_device.create(conn)
  table_user_device.create(conn)
  return True

if __name__ == '__main__':
  main()