import streamlit as st
import sys

if __name__ == '__main__':
    try:
        
        ########### Set page title and icon----------
        st.set_page_config(page_title="Stock Comparator", page_icon="bar_chart", layout="wide")
        
        ########### Display Page Title----------
        # st.sidebar.markdown("# Main Page")
        st.title("Stock Comparator 📊")
        st.write('This page gives insights into the comparision analysis between 2 or more stocks')
        st.markdown("---")
        
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
