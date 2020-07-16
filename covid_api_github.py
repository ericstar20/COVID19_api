def covid_api_sql():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    # API
    import requests
    import json
    # DB
    import pymysql
    from sqlalchemy import create_engine
    pymysql.install_as_MySQLdb()

    # AWS
    import aws_config

    # Set up API keys to get access permission
    def getStats(country):
      api_url = 'https://api.smartable.ai/coronavirus/stats/'+country
      api_params = {
        'Cache-Control': 'no-cache',
        'Subscription-Key': 'your key',
      }
      r = requests.get(url=api_url, params=api_params)
      return r.text

    # Get Data
    data = getStats('global')
    jsonData = json.loads(data)
    jsonData.keys()

    # Create three dataframe. One is Global total, the other is each country(state) info.

    # Global df
    update_T              = jsonData['updatedDateTime']
    totalConfirmedCases   = jsonData['stats']['totalConfirmedCases']
    newlyConfirmedCases   = jsonData['stats']['newlyConfirmedCases']
    totalDeaths           = jsonData['stats']['totalDeaths']
    newDeaths             = jsonData['stats']['newDeaths']
    totalRecoveredCases   = jsonData['stats']['totalRecoveredCases']
    newlyRecoveredCases   = jsonData['stats']['newlyRecoveredCases']

    global_list = [[update_T, totalConfirmedCases, totalDeaths, totalRecoveredCases, newlyConfirmedCases, newDeaths, newlyRecoveredCases]]
    global_col  = ['updateTime', 'totalConfirmedCases', 'totalDeaths', 'totalRecoveredCases', 'newlyConfirmedCases', 'newDeaths', 'newlyRecoveredCases']

    global_df = pd.DataFrame(data=global_list, columns = global_col)
    global_df['updateTime']=pd.to_datetime(global_df['updateTime'])
    #global_df.head()
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    # histroy df
    history_df = pd.DataFrame(jsonData['stats']['history'])
    history_df['date']=pd.to_datetime(history_df['date'])
    #history_df.head()
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Stats df
    stats = pd.DataFrame(jsonData['stats']['breakdowns'])
    location_norm = pd.json_normalize(stats['location'])
    stats_df = pd.concat([location_norm, stats], axis=1).drop('location', axis=1)
    stats_df['updateTime'] = update_T
    stats_df['updateTime']=pd.to_datetime(stats_df['updateTime'])
    #stats_df.head()
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Open database connection (local)
    db = pymysql.connect("host","name","password","database name" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    # print ("Database version : %s " % data)
    # disconnect from server
    db.close()
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Insert dfs to locl mysql
    engine = create_engine('mysql://name:password@host:port/database') #change to connect your mysql
    #if you want to create a new table
    global_df.to_sql(name='globalView',con=engine,if_exists='replace',index=False)
    history_df.to_sql(name='history',con=engine,if_exists='replace',index=False)
    stats_df.to_sql(name='statsView',con=engine,if_exists='replace',index=False)
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    # Open database connection (AWS)
    connection = pymysql.connect(host=aws_config.host,
                                 user=aws_config.user,
                                 password=aws_config.passwd)
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        #print("Database version: {} ".format(version[0]))

    # Insert dfs to locl mysql
    engine = create_engine('mysql://{}:{}@{}:{}/{}'.format(aws_config.user,aws_config.passwd,aws_config.host,aws_config.port,aws_config.db_name)) #change to connect your mysql

    #if you want to create a new table
    global_df.to_sql(name='globalView',con=engine,if_exists='replace',index=False)
    history_df.to_sql(name='history',con=engine,if_exists='replace',index=False)
    stats_df.to_sql(name='statsView',con=engine,if_exists='replace',index=False)
