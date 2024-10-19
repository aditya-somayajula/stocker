import streamlit as st
import pandas as pd
import sys
import common_functions

if __name__ == '__main__':
    try:
        
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
        
        feature_Set_list = ['ALL', 'Feature Set 1', 'Feature Set 2', 'Feature Set 3', 'Feature Set 4', 'Feature Set 5', 'Feature Set 6']
        model_list = ['ALL', 'Linear Regression', 'Decision Trees', 'Random Forest', 'XG Boost']

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
            analysis = st.radio('***Choose a Prediction Type***', ['Active Prediction', 'Passiv Prediction'], index=None, captions=['***Predict prices during trading window***', '***Predict prices post trading window***'], horizontal=True)
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
                    mkt_status_bool, mkt_status_data = common_functions.get_market_status(user_cookie)
                    if mkt_status_bool:
                        if mkt_status_data == 'Market is Closed':
                            st.warning('Unable to perform Active Prediction as market is closed. Active Prediction is enabled only during trading window.')
                        if mkt_status_data == 'Market is Open':
                            st.write('Active Prediction Code in progress. Stay Tuned...!!!')
                    else:
                        st.warning('Unable to get Market Status. Hence, unable to perform active prediction of prices. Contact administrator')
                else:
                    st.write('Passive Prediction Code in progress. Stay Tuned...!!!')
        else:
            st.write('Please make a selection to view predicted prices')
            
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
