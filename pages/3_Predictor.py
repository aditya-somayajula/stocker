import streamlit as st
import pandas as pd
import sys

if __name__ == '__main__':
    try:
        
        ########### Set page title and icon----------
        st.set_page_config(page_title='Stock Predictor', page_icon='triangular_ruler', layout='wide')
        
        ########### Display Page Title----------
        # st.sidebar.markdown("# Main Page")
        st.title('Stock Predictor 📐')
        st.write('This page gives insights into the possible price values of a stock')

        ip_file = 'config/Indices.csv'
        index_frame = pd.read_csv(ip_file, sep='|')
        index_frame = index_frame[['SYMBOL', 'COMPANY']].drop_duplicates(subset=['SYMBOL', 'COMPANY'], keep='first')
        index_frame['Options'] = index_frame['SYMBOL'] + ' (' + index_frame['COMPANY'] + ')'

        ########### Display initial options----------
        col1, col2, col3 = st.columns([1, 0.75, 1])
        with col1:
            symbol_select_option = st.selectbox('***Choose a Symbol***', sorted(list(index_frame['Options'])), index=0)
        with col3:
            user_cookie = st.text_input('***Cookie Value from NSE***', 
                                        help='To get Cookie value, go to the NSE website and look to download a CSV file of any symbol. The API call that gets triggered will have a cookie that can be accessed via Developer tools from a web browser')
        
        analysis = st.radio('***Please select prediction type***', ['Active Prediction', 'Passiv Prediction'], index=None,)
        result = st.button('Run Prediction', type='secondary')
        
        st.markdown('---')
        
        ########### Display Prediction Results----------
        if symbol_select_option is not None and result:
            st.write(f'Thank you for selecting {symbol_select_option} for comparision analysis. I\'m coming pretty soon.')
        else:
            st.write('Please make a selection...!!!')
        
        
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
