postgresql = {'host': 'db-hotel-management.c6i7hzivudlm.us-east-2.rds.amazonaws.com',
         'user': 'postgre',
         'passwd': 'postgresql',
         'db': 'postgres'}

postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])

