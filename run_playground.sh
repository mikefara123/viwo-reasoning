#!/bin/bash

# VCOIN Economic Playground Launcher
# Quick setup and launch script for the ViWo tokenomics playground

echo "🪙 VCOIN Economic Playground Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

echo "✅ pip3 found"

# Install requirements
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "Please check your internet connection and try again."
    exit 1
fi

# Launch playground
echo ""
echo "🚀 Launching VCOIN Economic Playground..."
echo "🌐 Open your browser to: http://localhost:8501"
echo ""
echo "📋 Available features:"
echo "  • Parameter Testing - Adjust tokenomics parameters"
echo "  • Price Discovery - Calculate initial token price"  
echo "  • Content Calculator - Test individual content rewards"
echo "  • A/B Comparison - Compare parameter configurations"
echo ""
echo "⚠️  Press Ctrl+C to stop the playground"
echo ""

# Run Streamlit app
streamlit run vcoin_playground.py

echo ""
echo "👋 Thanks for using VCOIN Economic Playground!"
