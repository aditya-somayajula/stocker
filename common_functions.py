# -*- coding: utf-8 -*-
'''
Created on Wed Oct  9 22:41:06 2024
@author: aditya
'''

# ---------- Importing Libraries ----------
# ---------- ---------- ---------- ---------- ----------
import json
import copy
import requests
import numpy as np
import pandas as pd
import streamlit as st
from io import StringIO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# from xgboost import XGBRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split



# --------- Configuration File ----------
# ---------- ---------- ---------- ---------- ----------
with open('config/config.json', encoding='utf-8') as cf:
    config_data = json.load(cf)



# ---------- Market Status API ----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def get_market_status(cke_val):
    mkt_data = ''
    try:
        url = 'https://www.nseindia.com/api/marketStatus'
        payload = {}
        headers = {
          'Accept': '*/*',
          'Connection': 'keep-alive',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'en-US,en;q=0.9',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Cache-Control': 'max-age=0',
          'Cookie': cke_val
        }
        
        response = requests.request('GET', url, headers=headers, data=payload)
        mkt_data = json.loads(response.text)
        
        if 'marketState' in mkt_data.keys():
            mkt_Frame = pd.DataFrame(mkt_data['marketState'])
            mkt_Frame = mkt_Frame[mkt_Frame['market'] == 'Capital Market']
            if len(mkt_Frame) != 0:
                return True, mkt_Frame.loc[0, 'marketStatus'], mkt_data
            else:
                return False, 'Unable to get Market Status', mkt_data
        else:
            return False, 'Unable to get Market Status', mkt_data
    
    except Exception as e:
        print(str(e))
        return False, 'Unable to get Market Status', mkt_data  



# ---------- Historical Data API ----------
# ---------- ---------- ---------- ---------- ----------  
@st.cache_data
def get_historical(stck, cke_val, from_date, to_date):
    try:
        url = 'https://www.nseindia.com/api/historical/cm/equity'
        para =  {
            'symbol': stck,
            "series": '[\"EQ\"]',
            'from': from_date,
            'to': to_date,
            'csv': 'true'
          }
        headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': cke_val,
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
          }
        response = requests.get(url, params=para, headers=headers)
        hist_Data = response.text
        csv_file = StringIO(hist_Data)
        historic_df = pd.read_csv(csv_file)
        
        return True, historic_df
    except Exception as e:
        print(str(e))
        return False, pd.DataFrame({})
 


# ---------- Pre-Process Historical Data ----------
# ---------- ---------- ---------- ---------- ----------  
@st.cache_data
def pre_process_historical(historic_df):
    try:
        historic_df.columns = ['Date', 'Series', 'Open', 'High', 'Low', 'Prev_Close', 'Last_Trading_Price', 'Close', 'Vol_Weighted_Avg_Price', '52W_High', '52W_Low', 'Volume', 'Value', 'No_of_Trade']
        
        for col in historic_df.columns:
          if col == 'Date' or col =='Series':
              continue
          historic_df[col] = historic_df[col].astype(str)
          historic_df[col] = historic_df[col].str.replace(',', '')
          historic_df[col] = pd.to_numeric(historic_df[col], errors='coerce')
        
        historic_df['Date'] = pd.to_datetime(historic_df['Date']).dt.date
        historic_df.drop(columns=['Series', 'Volume', 'Value', 'No_of_Trade'], inplace=True)
        historic_df = historic_df.sort_values(by='Date', ascending=False)
        
        return True, historic_df
    except Exception as e:
        print(str(e))
        return False, historic_df



# ---------- Feature Engineer Historical Data ----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def feature_engineer_historical(historic_df):
    try:
        historic_df['Change_Type'] = np.where(historic_df['Last_Trading_Price'] > historic_df['Open'], 1, np.where(historic_df['Last_Trading_Price'] < historic_df['Open'], -1, 0))
        
        bins = list(np.arange(0, 105, 10, dtype=int))
        labels = []
        for i in range(len(bins)):
            if i == len(bins) - 1 :
                break
            labels.append(str(bins[i]) + ' - ' + str(bins[i+1]))
        
        historic_df['High_Open'] = (((historic_df['High'] - historic_df['Open'])/historic_df['Open'])*100).round(2)
        historic_df['High_Open_Per'] = (historic_df['High_Open'].rank(pct=True) * 100).round(2)
        historic_df['High_Open_Per_Cat'] = pd.cut(historic_df['High_Open_Per'], bins=bins, labels=labels, right=False)
        historic_df['High_Open_Per_Cat'].fillna(labels[-1], inplace=True)
        
        historic_df['Low_Open'] = (((historic_df['Low'] - historic_df['Open'])/historic_df['Open'])*100).round(2)
        historic_df['Low_Open_Per'] = (historic_df['Low_Open'].rank(pct=True) * 100).round(2)
        historic_df['Low_Open_Per_Cat'] = pd.cut(historic_df['Low_Open_Per'], bins=bins, labels=labels, right=False)
        historic_df['Low_Open_Per_Cat'].fillna(labels[-1], inplace=True)
        
        historic_df['High_Low_Open_Avg'] = ((historic_df['High_Open'] + historic_df['Low_Open'])/2).round(2)
        historic_df['High_Low_Open_Avg_Per'] = (historic_df['High_Low_Open_Avg'].rank(pct=True) * 100).round(2)
        historic_df['High_Low_Open_Avg_Per_Cat'] = pd.cut(historic_df['High_Low_Open_Avg_Per'], bins=bins, labels=labels, right=False, include_lowest=True)
        historic_df['High_Low_Open_Avg_Per_Cat'].fillna(labels[-1], inplace=True)
        
        historic_df['LTP_Open'] = (((historic_df['Last_Trading_Price'] - historic_df['Open'])/historic_df['Open'])*100).round(2)
        historic_df['LTP_Open_Per'] = historic_df['LTP_Open'].rank(pct=True) * 100
        historic_df['LTP_Open_Per_Cat'] = pd.cut(historic_df['LTP_Open_Per'], bins=bins, labels=labels, right=False, include_lowest=True)
        historic_df['LTP_Open_Per_Cat'].fillna(labels[-1], inplace=True)
        
        return True, historic_df
    except Exception as e:
        print(str(e))
        return False, historic_df



# ---------- Historical Data ----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def historical(stck, cke_val):
    try:
        mkt_status_bool, mkt_status_data, mkt_data = get_market_status(cke_val)
        if mkt_status_bool == True:
            mkt_Frame = pd.DataFrame(mkt_data['marketState'])
            mkt_Frame = mkt_Frame[mkt_Frame['market'] == 'Capital Market']
            
            prediction_date = datetime.strptime(mkt_Frame.loc[0, 'tradeDate'], "%d-%b-%Y %H:%M")
            historic_to_date = prediction_date - timedelta(days=1)
            historic_from_date = historic_to_date - relativedelta(years=1)
            
            prediction_date_str = prediction_date.strftime("%d-%m-%Y")
            st.write('Prediction for Last Trading Price of ' + prediction_date_str)
            historic_to_date_str = historic_to_date.strftime("%d-%m-%Y")
            historic_from_date_str = historic_from_date.strftime("%d-%m-%Y")
            
            historic_bool, historic_df = get_historical(stck, cke_val, historic_from_date_str, historic_to_date_str)
            processed_bool, historic_df = pre_process_historical(historic_df)
            trans_bool, historic_df = feature_engineer_historical(historic_df)
            
            return True, historic_df
            
        else:
            False, pd.DataFrame({})        
    except Exception as e:
        print(str(e))
        return False, pd.DataFrame({})



# ---------- Today Data API ----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def get_today(stck, cke_val):
    try:
        url = 'ttps://www.nseindia.com/api/quote-equity'
        para =  {
              'symbol': stck
            }
        headers = {
              'Accept': '*/*',
              'Connection': 'keep-alive',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en-US,en;q=0.9',
              'Cookie': cke_val,
              'Cache-Control': 'max-age=0',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
              }
        
        response = requests.get(url, params=para, headers=headers)
        today_Data = json.loads(response.text)
        
        today_final_data = {}
        today_final_data['Date'] = datetime.strptime(today_Data['metadata']['lastUpdateTime'], '%d-%b-%Y %H:%M:%S').strftime('%d-%b-%Y')
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
        
        return True, today_df
        
    except Exception as e:
        print(str(e))
        return False, pd.DataFrame({})



# ---------- Current Data Chart API ----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def get_current(stck, cke_val):
    try:
        url = 'https://www.nseindia.com/api/chart-databyindex-dynamic'
        para =  {
                'index': stck + 'EQN',
                'type': 'symbol'
              }
        headers = {
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': cke_val,
                'Cache-Control': 'max-age=0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
              }
        response = requests.get(url, params=para, headers=headers)
        chart_Data = json.loads(response.text)
        current_df = pd.DataFrame(chart_Data['grapthData'], columns=['DateTime', 'Price', 'Mode'])
        
        return True, current_df
    except Exception as e: 
        print(str(e))
        return False, pd.DataFrame({})



# ---------- Pre-Process Current Data -----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def pre_process_current(current_df):
    try:
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
      
        cutoff_time = pd.to_datetime('15:30:02', format='%H:%M:%S').time()
        current_df_nm = current_df_nm[current_df_nm['Time'] <= cutoff_time]
        
        current_df_nm['High_Open'] = (((current_df_nm['High'] - current_df_nm['Open'])/current_df_nm['Open'])*100).round(2)
        current_df_nm['Low_Open'] = (((current_df_nm['Low'] - current_df_nm['Open'])/current_df_nm['Open'])*100).round(2)
        current_df_nm['High_Low_Open_Avg'] = ((current_df_nm['High_Open'] + current_df_nm['Low_Open'])/2).round(2)
        
        return True, current_df_nm
    except Exception as e:
        print(str(e))
        return False, current_df



# ---------- Current Data ----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def current(stck, cke_val):
    try:
        current_Bool, current_df = get_current(stck, cke_val)
        processed_bool, current_df = pre_process_current(current_df)
        
        st.markdown('<span>Actual Last Trading Price : </span><span style="color: red;">' + str(current_df["Price"].iloc[-1]) + '</span>',
            unsafe_allow_html=True)
        
        return True, current_df
    except Exception as e:
        print(str(e))
        return False, pd.DataFrame({})
    



# ---------- Passive Prediction ----------
# ---------- ---------- ---------- ---------- ----------
def passive_predict(stck, cke_val, feature_Val, model_Val):
    try:
        hist_Bool, hist_df = historical(stck, cke_val)
        curr_Bool, curr_df = current(stck, cke_val)
        
        X = hist_df.drop('LTP_Open', axis=1)
        y = hist_df[['LTP_Open']]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config_data['splitting']['test_size'], train_size=config_data['splitting']['test_size']
                                                            , random_state=42, shuffle=True)
        
        
        feature_dict = copy.deepcopy(config_data['features'])
        index_mapping = copy.deepcopy(config_data['features'])
        index_mapping = {key: ", ".join(value) if isinstance(value, list) else value for key, value in index_mapping.items()}
        index_mapping = {value: key for key, value in index_mapping.items()}
        if feature_Val == 'ALL':
            del feature_dict['ALL']
            feature_list = list(feature_dict.values())
        else:
            feature_list = [feature_dict[feature_Val]]
        
        model_dict = copy.deepcopy(config_data['models'])
        if model_Val == 'ALL':
            del model_dict['ALL']
            model_list = list(model_dict.keys())
        else:
            model_list = [model_dict[model_Val]]   
        
        if hist_Bool and curr_Bool:
            with st.spinner('Passive Prediction in progress...'):
                flat_features = [', '.join(item) for item in feature_list]
                
                # Model Analysis / Price Prediction ----------
                model_Frame = pd.DataFrame({}, columns=model_list, index=flat_features)
                pred_Frame = pd.DataFrame({}, columns=model_list, index=flat_features)
                for each_feature in feature_list:
                    for model in model_list:
                        
                        # Evaluate Model
                        temp_X_train = X_train[each_feature]
                        temp_X_test = X_test[each_feature]
                        if model == 'Linear Regression':
                            stocker_model = LinearRegression()
                            stocker_model.fit(temp_X_train, y_train)
                        elif model == 'Decision Trees':
                              stocker_model = DecisionTreeRegressor(random_state=1)
                              stocker_model.fit(temp_X_train, y_train)
                        elif model == 'Random Forest':
                              stocker_model = RandomForestRegressor(random_state=1)
                              stocker_model.fit(temp_X_train, y_train)
                        elif model == 'Ridge Regression':
                              stocker_model = Ridge(alpha=1)
                              stocker_model.fit(temp_X_train, y_train)
                        elif model == 'Lasso Regression':
                              stocker_model = Lasso(alpha=0.3)
                              stocker_model.fit(temp_X_train, y_train)
                        else:
                            continue
                        model_Frame.loc[', '.join(each_feature), model] = round(mean_absolute_error(y_test, stocker_model.predict(temp_X_test)), 2)
                        
                        # Prediction
                        pred_y = stocker_model.predict(curr_df[each_feature])
                        curr_df['LTP_Open'] = pred_y.round(2)
                        curr_df['PredictedLTP'] = (((curr_df['LTP_Open']/100) + 1) * curr_df['Open']).round(2)
                        pred_Frame.loc[', '.join(each_feature), model] = curr_df['PredictedLTP'].iloc[-1]
                        
                        
                st.write('Mean Absolute Error for each of the feature and algorithms. Lower the error, better the model...!!!')
                model_Frame.index = model_Frame.index.map(index_mapping)
                st.dataframe(model_Frame)
                
                st.write('')
                
                st.write('Predicted Last Trading Price for each of the feature and algorithms.')
                pred_Frame.index = pred_Frame.index.map(index_mapping)
                st.dataframe(pred_Frame)
                
                        
        else:
            st.warning('Unable to perform Passive Prediction. Please contact site administrator')
    except Exception as e:
        print(str(e))
        st.warning('Unable to perform Passive Prediction. Please contact site administrator')
        
