import streamlit as st
import pandas as pd
import sys
import json
import common_functions

if __name__ == '__main__':
    try:
        with open('E:/PythonScripts/Stocker/config/config.json', encoding='utf-8') as cf:
            config_data = json.load(cf)
            
            
        ########### Set page title and icon----------
        st.set_page_config(page_title='Stock Predictor', page_icon='triangular_ruler', layout='wide')
        
        
        ########### Display Page Title----------
        # st.sidebar.markdown("# Main Page")
        st.title('Stock Predictor 📐')
        st.write('This page gives insights into the possible price values of a stock')


        ########### Get Values----------
        ip_file = 'config/Indices.csv'
        index_frame = pd.read_csv(ip_file, sep='|')
        index_frame = index_frame[['SYMBOL', 'COMPANY']].drop_duplicates(subset=['SYMBOL', 'COMPANY'], keep='first')
        index_frame['Options'] = index_frame['SYMBOL'] + ' (' + index_frame['COMPANY'] + ')'
        
        feature_Set_list = list(config_data['features'].keys())
        model_list = list(config_data['models'].keys())


        ########### Display initial options----------
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            symbol_select_option = st.selectbox('***Choose a Symbol***', sorted(list(index_frame['Options'])), index=None)
        with col3:
            user_cookie = st.text_input('***Cookie Value from NSE***', value=None,
                                        help='To get Cookie value, go to the NSE website and look to download a CSV file of any symbol. The API call that gets triggered will have a cookie that can be accessed via Developer tools from a web browser')
        st.write('')
        
        col1, col2,col3 = st.columns([1, 1, 1])
        with col1:
            analysis = st.radio('***Choose a Prediction Type***', ['Active Prediction', 'Passive Prediction'], index=None, captions=['***Predict prices during trading window***', '***Predict prices post trading window***'], horizontal=True)
        with col2:
            feature_select_option = st.selectbox('***Choose a Feature Set***', feature_Set_list, index=None)
        with col3:
            model_select_option = st.selectbox('***Choose a Model***', model_list, index=None)
        result = st.button('Run Prediction', type='secondary')
        st.markdown('---')
        
        
        ########### Display Prediction Results----------
        if result:
            if symbol_select_option is None:
                st.warning('Please select a Symbol.')
            elif user_cookie is None:
                st.warning('Please provide cookie value.')
            elif analysis is None:
                st.warning('Please select a Prediction Type.')
            elif feature_select_option is None:
                st.warning('Please select a Feature Set.')
            elif model_select_option is None:
                st.warning('Please select a Model.')
            else:
                if analysis == 'Active Prediction':
                    mkt_status_bool, mkt_status_data, mkt_data = common_functions.get_market_status(user_cookie)
                    if mkt_status_bool:
                        if mkt_status_data == 'Closed':
                            st.warning('Unable to perform Active Prediction as market is closed. Active Prediction is enabled only during trading window.')
                        if mkt_status_data == 'Open':
                            st.write('Active Prediction Code in progress. Stay Tuned...!!!')
                    else:
                        st.warning('Unable to get Market Status. Hence, unable to perform active prediction of prices. Contact administrator')
                else:
                    common_functions.passive_predict(symbol_select_option.split(' (')[0], user_cookie, feature_select_option, model_select_option)
        else:
            st.write('Please make a selection to view predicted prices')
        
        
        ########### Display Page Footer---------- 
        footer = '''<div style='position:fixed;bottom:0;width:100%;background-color:transparent;text-align:center;padding:10px;font-size:16px;color:#ffffff;'>
            © 2024 Stocker. All Rights Reserved. Contact <a style='color:#ffa500;' href="mailto:adityas.sai@gmail.com">adityas.sai@gmail.com</a> for more information.
            </div>'''
        st.markdown(footer, unsafe_allow_html=True)
            
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
