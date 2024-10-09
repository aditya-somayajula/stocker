import streamlit as st
import sys

if __name__ == '__main__':
    try:
        
        ########### Set page title and icon----------
        st.set_page_config(page_title="Stock Profiler", page_icon="eyeglasses", layout="wide")
        
        ########### Display Page Title----------
        # st.sidebar.markdown("# Main Page")
        st.title("Stock Profiler 👓")
        st.write('This page gives insights into the profiling analysis - both fundamental and technical, of the individual stock')
        st.markdown("---")
        
    except Exception as e:
        # logging.error(e)
        print(e)
        sys.exit(0)
      
