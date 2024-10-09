# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 22:41:06 2024
@author: aditya
"""

# ---------- Importing Libraries ----------
import json
import requests
import pandas as pd
from io import StringIO
from datetime import datetime



# ---------- Get Historical Data from NSE ----------
# ---------- ---------- ---------- ---------- ----------
def get_historical(stck, cookie_val, from_date, to_date):

  # ----- Get Data -----
  url = "https://www.nseindia.com/api/historical/cm/equity"
  para =  {
        "symbol": stck,
        "series": "[\"EQ\"]",
        "from": from_date,
        "to": to_date,
        "csv": "true"
      }
  headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie_val,
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
      }
  response = requests.get(url, params=para, headers=headers)
  hist_Data = response.text
  csv_file = StringIO(hist_Data)
  historic_df = pd.read_csv(csv_file)

  # ----- Pre-Process the Data -----
  historic_df.columns = ['Date', 'Series', 'Open', 'High', 'Low', 'Prev_Close', 'Last_Trading_Price', 'Close', 'Vol_Weighted_Avg_Price', '52W_High', '52W_Low', 'Volume', 'Value', 'No_of_Trade']
  for col in historic_df.columns:
    if col == 'Date' or col =='Series':
        continue
    historic_df[col] = historic_df[col].astype(str)
    historic_df[col] = historic_df[col].str.replace(',', '')
    historic_df[col] = pd.to_numeric(historic_df[col], errors='coerce')
  historic_df['Date'] = pd.to_datetime(historic_df['Date']).dt.date
  historic_df.drop(columns=['Series', 'Prev_Close', '52W_High', '52W_Low', 'Volume', 'Value', 'No_of_Trade'], inplace=True)
  historic_df = historic_df.sort_values(by='Date', ascending=False)

  historic_df['High_Open'] = ((historic_df['High'] - historic_df['Open'])/historic_df['Open'])*100
  historic_df['High_Open'] = historic_df['High_Open'].round(2)
  historic_df['Low_Open'] = ((historic_df['Low'] - historic_df['Open'])/historic_df['Open'])*100
  historic_df['Low_Open'] = historic_df['Low_Open'].round(2)
  historic_df['High_Low_Open_Avg'] = ((historic_df['High_Open'] + historic_df['Low_Open'])/2).round(2)
  historic_df['LTP_Open'] = ((historic_df['Last_Trading_Price'] - historic_df['Open'])/historic_df['Open'])*100
  historic_df['LTP_Open'] = historic_df['LTP_Open'].round(2)

  # historic_df['High_LTP'] = ((historic_df['High'] - historic_df['Last_Trading_Price'])/historic_df['Last_Trading_Price'])*100
  # historic_df['High_LTP'] = historic_df['High_LTP'].round(2)
  # historic_df['Low_LTP'] = ((historic_df['Low'] - historic_df['Last_Trading_Price'])/historic_df['Last_Trading_Price'])*100
  # historic_df['Low_LTP'] = historic_df['Low_LTP'].round(2)

  return historic_df



# ---------- Get Today's Data from NSE ----------
# ---------- ---------- ---------- ---------- ----------
def get_today(stck, cookie_val):

  # ----- Get Data -----
  url = "https://www.nseindia.com/api/quote-equity"
  para =  {
        "symbol": stck
      }
  headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie_val,
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
  response = requests.get(url, params=para, headers=headers)

  # ----- Pre-Process the Data -----
  today_Data = json.loads(response.text)
  today_final_data = {}
  today_final_data['Date'] = datetime.strptime(today_Data['metadata']['lastUpdateTime'], "%d-%b-%Y %H:%M:%S").strftime("%d-%b-%Y")
  today_Data = today_Data['priceInfo']
  today_final_data['Open'] = today_Data['open']
  today_final_data['High'] = today_Data['intraDayHighLow']['max']
  today_final_data['Low'] = today_Data['intraDayHighLow']['min']
  today_final_data['Vol_Weighted_Avg_Price'] = today_Data['vwap']
  today_final_data['Last_Trading_Price'] = today_Data['lastPrice']
  if 'close' not in today_Data.keys():
    today_final_data['Close']  = ''
  else:
    today_final_data['Close'] = today_Data['close']
  today_df = pd.DataFrame(today_final_data, index=[0])

  for col in today_df.columns:
    if col == 'Date' or col =='Series':
        continue
    today_df[col] = today_df[col].astype(str)
    today_df[col] = today_df[col].str.replace(',', '')
    today_df[col] = pd.to_numeric(today_df[col], errors='coerce')
  today_df['High_Open'] = round(((today_df['High'] - today_df['Open'])/today_df['Open'])*100, 2)
  today_df['Low_Open'] = round(((today_df['Low'] - today_df['Open'])/today_df['Open'])*100, 2)

  return today_df



# ---------- Get Current Data Chart from NSE ----------
# ---------- ---------- ---------- ---------- ----------
def get_current(stck, cookie_val):

  # ----- Get Data -----
  url = "https://www.nseindia.com/api/chart-databyindex-dynamic"
  para =  {
        "index": stck + "EQN",
        "type": "symbol"
      }
  headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie_val,
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
      }
  response = requests.get(url, params=para, headers=headers)
  chart_Data = json.loads(response.text)
  current_df = pd.DataFrame(chart_Data['grapthData'], columns=['DateTime', 'Price', 'Mode'])

  # ----- Pre-Process the Data -----
  current_df['ModDateTime'] = pd.to_datetime(current_df['DateTime'], unit='ms')
  current_df['DateTime'] = pd.to_datetime(current_df['DateTime'], unit='ms').dt.strftime('%d/%m/%Y %H:%M:%S')
  current_df['Time'] = current_df['ModDateTime'].dt.time
  current_df_po = current_df[current_df['Mode'] == 'PO']
  current_df_po.reset_index(drop=True, inplace=True)
  current_df_nm = current_df[current_df['Mode'] == 'NM']
  current_df_nm.reset_index(drop=True, inplace=True)

  current_df_nm['Open'] = current_df_po['Price'].iloc[-1]
  current_df_nm['High'] = current_df_nm['Price'].iloc[0]
  current_df_nm['Low'] = current_df_nm['Price'].iloc[0]
  current_df_nm['High'] = current_df_nm['Price'].where(current_df_nm['Price'] > current_df_nm['High'].shift(1), current_df_nm['High'].shift(1)).cummax()
  current_df_nm['Low'] = current_df_nm['Price'].where(current_df_nm['Price'] < current_df_nm['Low'].shift(1), current_df_nm['Low'].shift(1)).cummin()
  current_df_nm.loc[0, 'High'] = current_df_nm.loc[0, 'Price']
  current_df_nm.loc[0, 'Low'] = current_df_nm.loc[0, 'Price']

  cutoff_time = pd.to_datetime('15:30:00', format='%H:%M:%S').time()
  current_df_nm = current_df_nm[current_df_nm['Time'] <= cutoff_time]
  current_df_nm['High_Open'] = ((current_df_nm['High'] - current_df_nm['Open'])/current_df_nm['Open'])*100
  current_df_nm['Low_Open'] = ((current_df_nm['Low'] - current_df_nm['Open'])/current_df_nm['Open'])*100
  current_df_nm['High_Open'] = current_df_nm['High_Open'].round(2)
  current_df_nm['Low_Open'] = current_df_nm['Low_Open'].round(2)
  current_df_nm['High_Low_Open_Avg'] = ((current_df_nm['High_Open'] + current_df_nm['Low_Open'])/2).round(2)

  return current_df_nm
