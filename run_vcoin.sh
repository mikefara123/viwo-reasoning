#!/bin/bash

# VCOIN V4 Tokenomics Platform
# Clean startup script

echo "🚀 Starting VCOIN V4 Tokenomics Platform..."
echo "📊 Hybrid Optimization Model Active"
echo "🎯 Target: $3+ RPM at $0.01 token price"
echo ""

# Kill any existing streamlit processes
pkill -f "streamlit run" 2>/dev/null || true

# Start the application
echo "🌐 Starting web application on http://localhost:8501"
python3 -m streamlit run vcoin_v4_comprehensive.py --server.port 8501

echo "✅ VCOIN Platform stopped"
