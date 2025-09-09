#!/bin/bash

# VCOIN Algorithm 5 Platform Launcher
# Sustainable Price Pool Distribution Model

echo "🚀 Starting VCOIN Algorithm 5 Platform..."
echo "📊 Price Pool Distribution Model"
echo "✅ Sustainable • Quality-Based • Multi-Stakeholder"
echo ""

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "❌ Streamlit not found. Installing..."
    pip3 install streamlit plotly pandas numpy
fi

# Launch the Algorithm 5 platform
echo "🌐 Launching on http://localhost:8501"
echo "📱 Algorithm 5: Sustainable tokenomics with fixed daily pool"
echo ""

python3 -m streamlit run algorithm_5/vcoin_algorithm_5_platform.py --server.port 8501 --server.headless true

echo ""
echo "✅ VCOIN Algorithm 5 Platform stopped"
