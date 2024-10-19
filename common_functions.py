# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 22:41:06 2024
@author: aditya
"""

# ---------- Importing Libraries ----------
# ---------- ---------- ---------- ---------- ----------
import streamlit as st
import json
import requests
import pandas as pd
from io import StringIO
from datetime import datetime
# ---------- ---------- ---------- ---------- ---------- 


# ---------- Market Status API ----------
# ---------- ---------- ---------- ---------- ----------
@st.cache_data
def get_market_status(cke_val):
    mkt_data = {}
    try:
        url = "https://www.nseindia.com/api/marketStatus"

        payload = {}
        headers = {
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'en-US,en;q=0.9',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Cache-Control': 'max-age=0',
          'Cookie': cke_val
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        mkt_data = json.loads(response.text)
        if 'marketState' in mkt_data.keys():
            mkt_Frame = pd.DataFrame(mkt_data['marketState'])
            mkt_Frame = mkt_Frame[mkt_Frame['market'] == 'Capital Market']
            if len(mkt_Frame) != 0:
                return True, mkt_Frame.loc[0, 'marketStatusMessage']
            else:
                return False, 'Unable to get Market Status'
        else:
            return False, 'Unable to get Market Status'
    
    except Exception as e:
        print(str(e))
        return False, 'Unable to get Market Status'
# ---------- ---------- ---------- ---------- ----------         
