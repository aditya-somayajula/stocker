import streamlit as st
import pandas as pd
import sys

if __name__ == '__main__':
    try:
        
        ########### Set page title and icon----------
        st.set_page_config(page_title="Stock Profiler", page_icon="eyeglasses", layout="wide")
        
        ########### Display Page Title----------
        # st.sidebar.markdown("# Main Page")
        st.title("Stock Profiler 👓")
        st.write('This page gives insights into the profiling analysis - both fundamental and technical, of the individual stock')

        # ip_file = 'config/Indices.csv'
        # index_frame = pd.read_csv(ip_file, sep='|')
        # index_frame['Options'] = index_frame['SYMBOL'] + ' (' + index_frame['COMPANY'] + ')'

        ########### Display initial options----------
        col1, col2, col3 = st.columns([1, 0.75, 1])
        # with col1:
        #     symbol_select_option = st.selectbox('Choose a Symbol:', sorted(list(index_frame['Options'])), index=0)
        with col3:
            user_cookie = st.text_input("Cookie Value from NSE", 
                                        help="""To get Cookie value, go to the NSE website and look to download a CSV file of any symbol. The API call that gets triggered will have a cookie that can be accessed via Developer tools from a web browser.""")
        
        st.markdown("---")
        
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
