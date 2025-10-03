#!/usr/bin/env python3
"""
Streamlit entry point for the Market Intelligence System
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaces.streamlit_app import main

if __name__ == "__main__":
    main()