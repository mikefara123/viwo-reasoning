#!/usr/bin/env python3
"""
VCOIN Algorithm 5 Platform - Streamlit Cloud Entry Point
This file is required by Streamlit Cloud for deployment
"""

import sys
import os

# Add the algorithm_5 directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithm_5'))

# Import and run the main application
try:
    from vcoin_algorithm_5_platform import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    import streamlit as st
    st.error(f"Failed to import main application: {str(e)}")
    st.write("Please ensure all dependencies are installed.")
    st.write("Required dependencies: streamlit, plotly")
    st.stop()
except Exception as e:
    import streamlit as st
    st.error(f"Application error: {str(e)}")
    st.write("Please contact support or check the application logs.")
    st.stop()
