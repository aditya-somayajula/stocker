# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 22:28:36 2024
@author: aditya
"""
import streamlit as st

########### Set page title and icon----------
st.set_page_config(page_title='Stocker - NSE Stock Predictor', page_icon='chart_with_upwards_trend', layout='wide')
st.write('# Welcome to Stocker...!!! 👋')

st.markdown(
    '''
    Stocker is an open-source stock price predicter web app built specifically 
    to provide various insights into the Symbols traded over the National Stock Exchange (NSE) - India.
    
    **👈 Select an option from the sidebar**
'''
)

html_title='<div style=\'padding: 10px; border: 3px solid #008080; border-radius: 10px; margin-bottom: 10px; background-color: #008080;\'><h1>Tile</h1><p>Content</p></div>'

col1, col2 = st.columns(2)
with col1:
    st.markdown(html_title.replace('Tile','752').replace('Content','Symbols'), unsafe_allow_html=True)
with col2:
    st.markdown(html_title.replace('Tile','74').replace('Content','Industries'), unsafe_allow_html=True)
    
col3, col4 = st.columns(2)
with col3:
    st.markdown(html_title.replace('Tile','57').replace('Content','Indices'), unsafe_allow_html=True)
with col4:
    st.markdown(html_title.replace('Tile','4').replace('Content','Segments'), unsafe_allow_html=True)

st.write('It is still work in progress. Stay Tuned...!!!')


########### Display Page Footer---------- 
footer = '''<div style='position:fixed;bottom:0;width:100%;background-color:transparent;text-align:center;padding:10px;font-size:16px;color:#ffffff;'>
    © 2024 Stocker. All Rights Reserved. Contact <a style='color:#ffa500;' href="mailto:adityas.sai@gmail.com">adityas.sai@gmail.com</a> for more information.
    </div>'''
st.markdown(footer, unsafe_allow_html=True)
