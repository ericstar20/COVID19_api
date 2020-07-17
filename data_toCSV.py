import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# API
import requests
import json

# Set up API keys to get access permission
def getStats(country):
  api_url = 'https://api.smartable.ai/coronavirus/stats/'+country
  api_params = {
    'Cache-Control': 'no-cache',
    'Subscription-Key': '90d024e3d92d4cde82bcfcbe3f0f3b46',
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# histroy df
history_df = pd.DataFrame(jsonData['stats']['history'])
history_df['date']=pd.to_datetime(history_df['date'])
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Stats df
stats = pd.DataFrame(jsonData['stats']['breakdowns'])
location_norm = pd.json_normalize(stats['location'])
stats_df = pd.concat([location_norm, stats], axis=1).drop('location', axis=1)
stats_df['updateTime'] = update_T
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Write dfs to a excel file
outputFile = "COVID19_Example_Data.xlsx"
with pd.ExcelWriter(outputFile) as ew:
    global_df.to_excel(ew, sheet_name="global", index=False)
    history_df.to_excel(ew, sheet_name="history" , index=False)
    stats_df.to_excel(ew, sheet_name="stats", index=False)
