import streamlit as st
import sys

if __name__ == '__main__':
    try:
        
        ########### Set page title and icon----------
        st.set_page_config(page_title="Stock Predictor", page_icon="triangular_ruler", layout="wide")
        
        ########### Display Page Title----------
        # st.sidebar.markdown("# Main Page")
        st.title("Stock Predictor 📐")
        st.write('This page gives insights into the possible price values of a stock')
        st.markdown("---")
        
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
