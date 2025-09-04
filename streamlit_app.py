"""
VCOIN Economic Playground - Main Entry Point for Streamlit Cloud
"""

import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

# Import the main playground
from vcoin_playground import main

if __name__ == "__main__":
    main()
