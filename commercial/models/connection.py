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