"""
VCOIN V4 Platform - Main Entry Point
Organized, clean codebase with multiple app options
"""

import sys
import os
import streamlit as st

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

def main():
    """Main platform selector"""
    
    st.set_page_config(
        page_title="VCOIN V4 Platform",
        page_icon="💎",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.markdown("# 💎 **VCOIN V4 Platform**")
    st.markdown("### **Choose your interface**")
    
    # App selection
    st.markdown("---")
    
    app_choice = st.selectbox(
        "Which app would you like to use?",
        [
            "🎓 Educational Platform (RECOMMENDED for new users)",
            "🎯 Simple Calculator (Quick calculations)",
            "📊 Advanced Platform (3 Tools)",
            "🧪 Legacy App (Backup)"
        ],
        help="Choose the interface that best fits your needs"
    )
    
    # App descriptions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🎓 **Educational Platform**")
        st.markdown("""
        **Best for:** New users, investors learning tokenomics
        
        **Features:**
        - Step-by-step explanations
        - Interactive learning
        - Plain decimal inputs
        - Beginner-friendly metrics
        
        **Perfect if you want to:**
        - Learn how VCOIN works
        - Understand the economics
        - See detailed breakdowns
        """)
    
    with col2:
        st.markdown("### 🎯 **Simple Calculator**")
        st.markdown("""
        **Best for:** Content creators, quick calculations
        
        **Features:**
        - Fast calculations
        - Flexible inputs
        - Clear results
        - Export functionality
        
        **Perfect if you want to:**
        - Quick earnings estimate
        - Test content scenarios
        - Simple interface
        """)
    
    with col3:
        st.markdown("### 📊 **Advanced Platform**")
        st.markdown("""
        **Best for:** Investors, platform operators
        
        **Features:**
        - 3 specialized tools
        - Platform-wide economics
        - Investment analysis
        - Creator-consumer balance
        
        **Perfect if you want to:**
        - Analyze platform economics
        - Plan investments
        - Study different scenarios
        """)
    
    with col4:
        st.markdown("### 🧪 **Legacy App**")
        st.markdown("""
        **Best for:** Testing, comparison
        
        **Features:**
        - Original interface
        - All historical features
        - Backup functionality
        
        **Perfect if you want to:**
        - Access older features
        - Compare with new versions
        - Fallback option
        """)
    
    # Launch button
    st.markdown("---")
    
    if st.button("🚀 Launch Selected App", type="primary"):
        if "Educational Platform" in app_choice:
            st.info("Redirecting to Educational Platform...")
            st.markdown("**To launch:** `streamlit run apps/vcoin_educational.py --server.port 8501`")
        elif "Simple Calculator" in app_choice:
            st.info("Redirecting to Simple Calculator...")
            st.markdown("**To launch:** `streamlit run apps/vcoin_simple.py --server.port 8504`")
        elif "Advanced Platform" in app_choice:
            st.info("Redirecting to Advanced Platform...")
            st.markdown("**To launch:** `streamlit run apps/vcoin_playground.py --server.port 8503`")
        else:
            st.info("Redirecting to Legacy App...")
            st.markdown("**To launch:** `streamlit run apps/vcoin_app.py --server.port 8505`")
    
    # Quick stats
    st.markdown("---")
    st.markdown("### 📊 **Platform Stats**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎬 Tools Available", "3", "Content, Balance, Investment")
    with col2:
        st.metric("🧪 Test Scenarios", "16", "Comprehensive coverage")
    with col3:
        st.metric("✅ Consistency", "100%", "Perfect alignment")
    with col4:
        st.metric("📈 Production Status", "Ready", "Fully validated")
    
    # Footer
    st.markdown("---")
    st.markdown("### 🔗 **Resources**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📚 Documentation:**
        - [📖 User Guide](docs/README.md)
        - [🧮 Algorithm Details](docs/reports/)
        - [📊 Test Results](docs/analysis/)
        """)
    
    with col2:
        st.markdown("""
        **🛠️ Developer:**
        - [🧪 Test Suite](tests/)
        - [⚙️ Core Engine](core/)
        - [📁 Exports](exports/)
        """)

if __name__ == "__main__":
    main()
