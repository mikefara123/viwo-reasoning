# 🚀 Launch Commands for Algorithm 5 Platform

## ✅ Fixed Launch Options

The startup script has been fixed to use the correct Python module syntax. Here are your options:

### Option 1: Using the Fixed Startup Script
```bash
./run_algorithm_5.sh
```

### Option 2: Direct Launch (Recommended)
```bash
./launch_direct.sh
```

### Option 3: Manual Command
```bash
python3 -m streamlit run algorithm_5/vcoin_algorithm_5_platform.py --server.port 8501
```

### Option 4: Background Launch
```bash
python3 -m streamlit run algorithm_5/vcoin_algorithm_5_platform.py --server.port 8501 --server.headless true &
```

## 🌐 Access the Platform

Once launched, the platform will be available at:
**http://localhost:8501**

## 🔧 Troubleshooting

### If you get "command not found: streamlit"
The issue was that `streamlit` wasn't in the PATH. The fix is to use:
```bash
python3 -m streamlit run [file]
```
Instead of:
```bash
streamlit run [file]
```

### If you get import errors
Make sure dependencies are installed:
```bash
pip3 install streamlit plotly pandas numpy
```

### If port 8501 is busy
Use a different port:
```bash
python3 -m streamlit run algorithm_5/vcoin_algorithm_5_platform.py --server.port 8502
```

## ✅ Platform Features

Once launched, you'll have access to:
1. **🧮 Algorithm Overview** - Theory and benefits
2. **⚙️ Pool Configuration** - Market parameters  
3. **📊 Platform Simulation** - Real-time economics
4. **🧪 Scenario Analysis** - Multi-scale testing
5. **🧮 Content Calculator** - Interactive rewards

**The platform is now ready to use!** 🎉
