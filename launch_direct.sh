#!/bin/bash

# Direct launch without background process
echo "🚀 Launching VCOIN Algorithm 5 Platform..."
echo "📊 Direct launch on http://localhost:8501"
echo ""

# Launch directly
python3 -m streamlit run algorithm_5/vcoin_algorithm_5_platform.py --server.port 8501

echo ""
echo "✅ Platform stopped"
