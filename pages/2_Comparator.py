import streamlit as st
import pandas as pd
import sys

if __name__ == '__main__':
    try:
        
        ########### Set page title and icon----------
        st.set_page_config(page_title='Stock Comparator', page_icon='bar_chart', layout='wide')
        
        
        ########### Display Page Title----------
        # st.sidebar.markdown("# Main Page")
        st.title('Stock Comparator 📊')
        st.write('This page gives insights into the comparision analysis between 2 or more stocks')
        
        
        ########### Get Values----------
        ip_file = 'config/Indices.csv'
        index_frame = pd.read_csv(ip_file, sep='|')
        index_frame = index_frame[['SYMBOL', 'COMPANY']].drop_duplicates(subset=['SYMBOL', 'COMPANY'], keep='first')
        index_frame['Options'] = index_frame['SYMBOL'] + ' (' + index_frame['COMPANY'] + ')'


        ########### Display initial options----------
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            symbol_select_option = st.multiselect('***Choose a Symbol(s)***', sorted(list(index_frame['Options'])))
        with col3:
            user_cookie = st.text_input("***Cookie Value from NSE***", value=None,
                                        help='To get Cookie value, go to the NSE website and look to download a CSV file of any symbol. The API call that gets triggered will have a cookie that can be accessed via Developer tools from a web browser')
        st.write('')
        
        result = st.button('Run Comparision', type='secondary')
        st.markdown('---')
        
        
        ########### Display Comparision Results----------        
        if symbol_select_option is not None and result:
            st.write(f'Thank you for selecting {symbol_select_option} for comparision analysis. I\'m coming pretty soon.')
        else:
            st.write('Please make a selection...!!!')
        
        
        ########### Display Page Footer---------- 
        footer = '''<div style='position:fixed;bottom:0;width:100%;background-color:transparent;text-align:center;padding:10px;font-size:16px;color:#ffffff;'>
            © 2024 Stocker. All Rights Reserved. Contact <a style='color:#ffa500;' href="mailto:adityas.sai@gmail.com">adityas.sai@gmail.com</a> for more information.
            </div>'''
        st.markdown(footer, unsafe_allow_html=True)
        
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
