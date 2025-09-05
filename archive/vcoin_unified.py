"""
VCOIN V4 - Unified Platform
All functionality in one web app with multiple tabs
Single command deployment: streamlit run vcoin_unified.py
"""

import streamlit as st
import math
from datetime import datetime
import json

def safe_import_check():
    """Check if optional dependencies are available"""
    dependencies = {}
    
    try:
        import pandas as pd
        dependencies['pandas'] = pd
    except ImportError:
        dependencies['pandas'] = None
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        dependencies['plotly_express'] = px
        dependencies['plotly_go'] = go
    except ImportError:
        dependencies['plotly_express'] = None
        dependencies['plotly_go'] = None
    
    return dependencies

def create_safe_chart(x_values, y_values, title, chart_type="bar"):
    """Create charts with fallback to text if plotly unavailable"""
    deps = st.session_state.get('dependencies', {})
    
    if deps.get('plotly_express') and deps.get('plotly_go'):
        # Use plotly if available
        px = deps['plotly_express']
        go = deps['plotly_go']
        
        if chart_type == "bar":
            fig = px.bar(x=x_values, y=y_values, title=title)
        elif chart_type == "line":
            fig = px.line(x=x_values, y=y_values, title=title)
        elif chart_type == "pie":
            fig = px.pie(values=y_values, names=x_values, title=title)
        else:
            fig = px.bar(x=x_values, y=y_values, title=title)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback to text representation
        st.markdown(f"### {title}")
        if not y_values or max(y_values) == 0:
            st.write("No data to display")
            return
        
        max_val = max(y_values)
        st.markdown("```")
        for x, y in zip(x_values, y_values):
            bar_length = int((y / max_val) * 20) if max_val > 0 else 0
            bar = "█" * bar_length
            st.write(f"{x}: {bar} {y:,.2f}")
        st.markdown("```")

def create_safe_dataframe(data, title="Data"):
    """Create dataframe with fallback if pandas unavailable"""
    deps = st.session_state.get('dependencies', {})
    
    if deps.get('pandas'):
        pd = deps['pandas']
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        # Fallback to simple table
        st.markdown(f"### {title}")
        if isinstance(data, list) and data:
            # Display as simple table
            for i, row in enumerate(data):
                if isinstance(row, dict):
                    cols = st.columns(len(row))
                    for j, (key, value) in enumerate(row.items()):
                        cols[j].write(f"**{key}:** {value}")
                    if i < len(data) - 1:
                        st.markdown("---")

def educational_interface():
    """Educational interface for learning tokenomics"""
    
    st.markdown("# 🎓 **Learn VCOIN V4 Tokenomics**")
    st.markdown("### **Step-by-step guide for beginners**")
    
    # Introduction
    with st.expander("👋 **New to VCOIN? Start Here!**", expanded=True):
        st.markdown("""
        **Welcome to VCOIN V4!** This shows you exactly how content creators earn money.
        
        **🎯 What You'll Learn:**
        - How your content creates real economic value
        - How community engagement attracts investment  
        - How creators get paid in USD (not just tokens)
        - Why this system is sustainable long-term
        """)
    
    # Input Section
    st.markdown("## 📝 **Your Content & Settings**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **🎬 Content Performance**")
        
        views = st.number_input(
            "**Views** (How many people watched?)",
            min_value=0.0,
            value=10000.0,
            step=100.0,
            help="Total number of people who viewed your content"
        )
        
        engagement_rate = st.number_input(
            "**Engagement Rate %** (Likes, shares, comments)",
            min_value=0.0,
            max_value=100.0,
            value=15.0,
            step=0.1,
            help="Percentage of viewers who engaged"
        )
        
        shares = st.number_input(
            "**Shares** (How many times shared?)",
            min_value=0.0,
            value=views * (engagement_rate/100) * 0.1,
            step=1.0,
            help="Number of times your content was shared"
        )
        
        comments = st.number_input(
            "**Comments** (How many comments?)",
            min_value=0.0,
            value=views * (engagement_rate/100) * 0.05,
            step=1.0,
            help="Number of comments on your content"
        )
    
    with col2:
        st.markdown("### **💰 Platform Economics**")
        
        token_price = st.number_input(
            "**VCOIN Price** (USD per token)",
            min_value=0.01,
            value=1.50,
            step=0.01,
            help="Current market price of one VCOIN token"
        )
        
        total_users = st.number_input(
            "**Platform Users** (Total active users)",
            min_value=1.0,
            value=100000.0,
            step=1000.0,
            help="Total number of active users on the platform"
        )
        
        creator_percentage = st.number_input(
            "**Creator Share %** (What % goes to creators?)",
            min_value=0.0,
            max_value=100.0,
            value=55.0,
            step=1.0,
            help="Percentage of generated value that goes to content creators"
        )
    
    # Calculations
    likes_reactions = views * (engagement_rate/100) * 0.7
    total_interactions = views + (shares * 5) + likes_reactions + (comments * 3)
    
    community_value_per_interaction = 0.50
    base_community_value = total_interactions * community_value_per_interaction
    
    engagement_multiplier = 1.0 + (engagement_rate / 100 * 2.0)
    enhanced_community_value = base_community_value * engagement_multiplier
    
    market_efficiency = 0.85
    investment_conversion = 0.75
    
    theoretical_investment = enhanced_community_value * 50
    actual_investment = theoretical_investment * market_efficiency * investment_conversion
    
    base_price = 1.0
    price_appreciation_factor = token_price / base_price
    reward_multiplier = max(0.2, min(1.0, 1.0 / (price_appreciation_factor ** 0.3)))
    
    creator_value_share = actual_investment * (creator_percentage / 100)
    adjusted_creator_value = creator_value_share * reward_multiplier
    
    tokens_earned = adjusted_creator_value / token_price
    rpm = (adjusted_creator_value / views) * 1000 if views > 0 else 0
    
    # Results
    st.markdown("---")
    st.markdown("## 🎯 **Your Earnings**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💵 USD Earnings", f"${adjusted_creator_value:,.2f}", help="What you earn in dollars")
    
    with col2:
        st.metric("🪙 VCOIN Tokens", f"{tokens_earned:,.2f}", help="Tokens you receive")
    
    with col3:
        st.metric("📊 Value Created", f"${enhanced_community_value:,.2f}", help="Total community value")
    
    with col4:
        st.metric("💰 Investment Attracted", f"${actual_investment:,.2f}", help="Investment your content brought")
    
    # Detailed explanation
    with st.expander("🔍 **See How We Calculated This**"):
        st.markdown(f"""
        **1. Engagement Calculation:**
        - Views: {views:,.0f}
        - Shares: {shares:,.0f} (worth 5x in algorithm)
        - Likes/Reactions: {likes_reactions:,.0f}
        - Comments: {comments:,.0f} (worth 3x in algorithm)
        - **Total Weighted Interactions: {total_interactions:,.0f}**
        
        **2. Community Value Generation:**
        - Base Value: {total_interactions:,.0f} × $0.50 = ${base_community_value:,.2f}
        - Engagement Multiplier: 1.0 + ({engagement_rate:.1f}% × 2.0) = {engagement_multiplier:.2f}x
        - **Enhanced Value: ${enhanced_community_value:,.2f}**
        
        **3. Investment Attraction:**
        - Theoretical Investment: ${enhanced_community_value:,.2f} × 50 = ${theoretical_investment:,.2f}
        - Market Efficiency: {market_efficiency:.0%}
        - Conversion Rate: {investment_conversion:.0%}
        - **Actual Investment: ${actual_investment:,.2f}**
        
        **4. Creator Rewards:**
        - Creator Share: {creator_percentage:.0f}% of ${actual_investment:,.2f} = ${creator_value_share:,.2f}
        - Price Adjustment: Token price ${token_price:.2f} → Multiplier {reward_multiplier:.3f}x
        - **Final USD Value: ${adjusted_creator_value:,.2f}**
        - **Tokens Earned: {tokens_earned:,.2f} VCOIN**
        - **Revenue per 1000 views: ${rpm:.2f}**
        """)
    
    return {
        'views': views,
        'engagement_rate': engagement_rate,
        'shares': shares,
        'comments': comments,
        'token_price': token_price,
        'total_users': total_users,
        'creator_percentage': creator_percentage,
        'adjusted_creator_value': adjusted_creator_value,
        'tokens_earned': tokens_earned,
        'enhanced_community_value': enhanced_community_value,
        'actual_investment': actual_investment,
        'rpm': rpm
    }

def content_calculator_interface():
    """Content calculator for individual pieces"""
    
    st.markdown("# 🎬 **Content Calculator**")
    st.markdown("### **Calculate earnings for individual content**")
    
    # Quick scenarios
    st.markdown("### 🚀 **Quick Scenarios**")
    col1, col2, col3, col4 = st.columns(4)
    
    scenarios = [
        ("📱 Small", 1000, 15.0),
        ("🌟 Popular", 10000, 23.0),
        ("🔥 Viral", 100000, 18.5),
        ("💥 Mega", 1000000, 22.0)
    ]
    
    for i, (name, views, engagement) in enumerate(scenarios):
        with [col1, col2, col3, col4][i]:
            if st.button(f"{name}\n{views:,} views", use_container_width=True):
                st.session_state.scenario_views = views
                st.session_state.scenario_engagement = engagement
    
    # Input section
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **📊 Content Metrics**")
        
        view_count = st.number_input(
            "Views",
            min_value=0.0,
            value=st.session_state.get('scenario_views', 10000.0),
            step=100.0
        )
        
        engagement_rate = st.number_input(
            "Engagement Rate %",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.get('scenario_engagement', 15.0),
            step=0.1
        )
        
        shares = st.number_input(
            "Shares",
            min_value=0.0,
            value=view_count * (engagement_rate/100) * 0.1,
            step=1.0
        )
        
        likes = st.number_input(
            "Likes",
            min_value=0.0,
            value=view_count * (engagement_rate/100) * 0.6,
            step=1.0
        )
        
        dislikes = st.number_input(
            "Dislikes",
            min_value=0.0,
            value=view_count * (engagement_rate/100) * 0.05,
            step=1.0
        )
        
        comments = st.number_input(
            "Comments",
            min_value=0.0,
            value=view_count * (engagement_rate/100) * 0.05,
            step=1.0
        )
    
    with col2:
        st.markdown("### **⚙️ Platform Settings**")
        
        vcoin_price = st.number_input(
            "VCOIN Price (USD)",
            min_value=0.01,
            value=1.50,
            step=0.01
        )
        
        platform_users = st.number_input(
            "Platform Users",
            min_value=1.0,
            value=100000.0,
            step=1000.0
        )
        
        # V4 Distribution percentages
        st.markdown("**V4 Distribution:**")
        creator_share = 55.0
        consumer_share = 25.0
        platform_share = 12.0
        ecosystem_share = 8.0
        
        st.write(f"• Creators: {creator_share}%")
        st.write(f"• Consumers: {consumer_share}%") 
        st.write(f"• Platform: {platform_share}%")
        st.write(f"• Ecosystem: {ecosystem_share}%")
    
    # V4 Calculations
    total_interactions = view_count + (shares * 5) + likes + dislikes + (comments * 3)
    
    # V4 Community value (optimized)
    community_value_factor = 0.50
    base_community_value = total_interactions * community_value_factor
    
    # V4 Engagement multiplier
    engagement_multiplier = 1.0 + (engagement_rate / 100 * 2.0)
    enhanced_community_value = base_community_value * engagement_multiplier
    
    # V4 Investment attraction
    market_efficiency = 0.85
    investment_conversion = 0.75
    theoretical_investment = enhanced_community_value * 50
    actual_investment = theoretical_investment * market_efficiency * investment_conversion
    
    # V4 Dynamic reward adjustment
    base_price = 1.0
    price_appreciation_factor = vcoin_price / base_price
    reward_multiplier = max(0.2, min(1.0, 1.0 / (price_appreciation_factor ** 0.3)))
    
    # Distribution calculation
    total_vcoin = actual_investment / vcoin_price
    adjusted_total_vcoin = total_vcoin * reward_multiplier
    
    creator_vcoin = adjusted_total_vcoin * (creator_share / 100)
    creator_usd = creator_vcoin * vcoin_price
    
    consumer_vcoin = adjusted_total_vcoin * (consumer_share / 100)
    platform_vcoin = adjusted_total_vcoin * (platform_share / 100)
    ecosystem_vcoin = adjusted_total_vcoin * (ecosystem_share / 100)
    
    # Results
    st.markdown("---")
    st.markdown("## 🎯 **Results**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💵 Creator USD", f"${creator_usd:,.2f}")
        st.metric("🪙 Creator VCOIN", f"{creator_vcoin:,.2f}")
    
    with col2:
        st.metric("📊 Total Value", f"${enhanced_community_value:,.2f}")
        st.metric("💰 Investment", f"${actual_investment:,.2f}")
    
    with col3:
        rpm = (creator_usd / view_count) * 1000 if view_count > 0 else 0
        st.metric("📈 RPM", f"${rpm:.2f}")
        st.metric("⚡ Interactions", f"{total_interactions:,.0f}")
    
    # Distribution breakdown
    st.markdown("### **💰 Token Distribution**")
    
    distribution_data = [
        {"Recipient": "Creator", "VCOIN": f"{creator_vcoin:,.2f}", "USD": f"${creator_usd:,.2f}", "Share": f"{creator_share}%"},
        {"Recipient": "Consumers", "VCOIN": f"{consumer_vcoin:,.2f}", "USD": f"${consumer_vcoin * vcoin_price:,.2f}", "Share": f"{consumer_share}%"},
        {"Recipient": "Platform", "VCOIN": f"{platform_vcoin:,.2f}", "USD": f"${platform_vcoin * vcoin_price:,.2f}", "Share": f"{platform_share}%"},
        {"Recipient": "Ecosystem", "VCOIN": f"{ecosystem_vcoin:,.2f}", "USD": f"${ecosystem_vcoin * vcoin_price:,.2f}", "Share": f"{ecosystem_share}%"}
    ]
    
    create_safe_dataframe(distribution_data, "Distribution Breakdown")
    
    return {
        'creator_usd': creator_usd,
        'creator_vcoin': creator_vcoin,
        'total_value': enhanced_community_value,
        'rpm': rpm
    }

def creator_consumer_balance_interface():
    """Creator-consumer balance calculator"""
    
    st.markdown("# ⚖️ **Creator-Consumer Balance**")
    st.markdown("### **Platform-wide economics analysis**")
    
    # Platform inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **📊 Platform Scale**")
        
        total_users = st.number_input(
            "Total Users",
            min_value=1000.0,
            value=100000.0,
            step=1000.0
        )
        
        daily_content_pieces = st.number_input(
            "Daily Content Pieces",
            min_value=1.0,
            value=total_users * 0.1,  # 10% of users create content daily
            step=100.0
        )
        
        avg_views_per_content = st.number_input(
            "Average Views per Content",
            min_value=1.0,
            value=500.0,
            step=10.0
        )
        
        avg_engagement_rate = st.number_input(
            "Average Engagement Rate %",
            min_value=0.0,
            max_value=100.0,
            value=12.0,
            step=0.1
        )
    
    with col2:
        st.markdown("### **💰 Economic Settings**")
        
        starting_token_price = st.number_input(
            "Starting VCOIN Price (USD)",
            min_value=0.01,
            value=1.00,
            step=0.01
        )
        
        target_inflation = st.number_input(
            "Target Annual Inflation %",
            min_value=0.0,
            max_value=20.0,
            value=8.0,
            step=0.1
        )
        
        # Distribution settings
        st.markdown("**Distribution:**")
        creator_pct = 55.0
        consumer_pct = 25.0
        platform_pct = 12.0
        ecosystem_pct = 8.0
        
        st.write(f"• Creators: {creator_pct}%")
        st.write(f"• Consumers: {consumer_pct}%")
        st.write(f"• Platform: {platform_pct}%") 
        st.write(f"• Ecosystem: {ecosystem_pct}%")
    
    # Platform-wide calculations
    daily_total_views = daily_content_pieces * avg_views_per_content
    daily_total_engagement = daily_total_views * (avg_engagement_rate / 100)
    
    # Estimate shares and comments from engagement
    daily_shares = daily_total_engagement * 0.1
    daily_comments = daily_total_engagement * 0.05
    daily_likes = daily_total_engagement * 0.85
    
    # Total weighted interactions
    daily_interactions = daily_total_views + (daily_shares * 5) + daily_likes + (daily_comments * 3)
    
    # Community value (platform-wide uses same factor as individual content)
    community_value_factor = 0.50
    daily_base_value = daily_interactions * community_value_factor
    
    # Platform-wide engagement multiplier
    engagement_multiplier = 1.0 + (avg_engagement_rate / 100 * 2.0)
    daily_enhanced_value = daily_base_value * engagement_multiplier
    
    # Investment attraction
    market_efficiency = 0.85
    investment_conversion = 0.75
    daily_theoretical_investment = daily_enhanced_value * 50
    daily_actual_investment = daily_theoretical_investment * market_efficiency * investment_conversion
    
    # Monthly and annual projections
    monthly_investment = daily_actual_investment * 30
    annual_investment = daily_actual_investment * 365
    
    # Token economics
    price_appreciation_factor = starting_token_price / 1.0
    reward_multiplier = max(0.2, min(1.0, 1.0 / (price_appreciation_factor ** 0.3)))
    
    daily_tokens_generated = daily_actual_investment / starting_token_price
    adjusted_daily_tokens = daily_tokens_generated * reward_multiplier
    
    # Distribution
    daily_creator_tokens = adjusted_daily_tokens * (creator_pct / 100)
    daily_creator_usd = daily_creator_tokens * starting_token_price
    
    daily_consumer_tokens = adjusted_daily_tokens * (consumer_pct / 100)
    daily_platform_tokens = adjusted_daily_tokens * (platform_pct / 100)
    daily_ecosystem_tokens = adjusted_daily_tokens * (ecosystem_pct / 100)
    
    # Per creator metrics
    active_creators = daily_content_pieces  # Assuming 1 piece per creator per day
    usd_per_creator_per_day = daily_creator_usd / active_creators if active_creators > 0 else 0
    tokens_per_creator_per_day = daily_creator_tokens / active_creators if active_creators > 0 else 0
    
    # Results
    st.markdown("---")
    st.markdown("## 📊 **Platform Economics**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Daily Active Creators", f"{active_creators:,.0f}")
        st.metric("💵 USD per Creator/Day", f"${usd_per_creator_per_day:,.2f}")
    
    with col2:
        st.metric("📊 Daily Platform Value", f"${daily_enhanced_value:,.2f}")
        st.metric("💰 Daily Investment", f"${daily_actual_investment:,.2f}")
    
    with col3:
        st.metric("🪙 Daily Tokens Generated", f"{adjusted_daily_tokens:,.2f}")
        st.metric("📈 Monthly Investment", f"${monthly_investment:,.2f}")
    
    with col4:
        st.metric("⚡ Daily Interactions", f"{daily_interactions:,.0f}")
        st.metric("🎯 Annual Investment", f"${annual_investment:,.2f}")
    
    # Sustainability analysis
    st.markdown("### **🔄 Sustainability Metrics**")
    
    # Calculate inflation rate
    annual_tokens_generated = adjusted_daily_tokens * 365
    # Assume initial supply (this would be configurable in real implementation)
    initial_token_supply = 1000000  # 1M tokens
    actual_inflation_rate = (annual_tokens_generated / initial_token_supply) * 100
    
    sustainability_data = [
        {"Metric": "Target Inflation", "Value": f"{target_inflation:.1f}%", "Status": "🎯 Target"},
        {"Metric": "Actual Inflation", "Value": f"{actual_inflation_rate:.1f}%", "Status": "✅ Healthy" if 5 <= actual_inflation_rate <= 15 else "⚠️ Review"},
        {"Metric": "Market Efficiency", "Value": f"{market_efficiency:.0%}", "Status": "✅ Optimized"},
        {"Metric": "Investment Conversion", "Value": f"{investment_conversion:.0%}", "Status": "✅ Strong"},
        {"Metric": "Creator Coverage", "Value": f"${usd_per_creator_per_day:.2f}/day", "Status": "✅ Competitive" if usd_per_creator_per_day > 10 else "⚠️ Low"}
    ]
    
    create_safe_dataframe(sustainability_data, "Sustainability Analysis")
    
    return {
        'daily_creator_usd': daily_creator_usd,
        'usd_per_creator': usd_per_creator_per_day,
        'daily_investment': daily_actual_investment,
        'inflation_rate': actual_inflation_rate
    }

def investment_analysis_interface():
    """Investment analysis and projections"""
    
    st.markdown("# 💎 **Investment Analysis**")
    st.markdown("### **Long-term economic projections**")
    
    # Investment parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **📈 Growth Projections**")
        
        initial_users = st.number_input(
            "Initial Users",
            min_value=1000.0,
            value=50000.0,
            step=1000.0
        )
        
        monthly_growth_rate = st.number_input(
            "Monthly User Growth %",
            min_value=0.0,
            max_value=50.0,
            value=15.0,
            step=0.1
        )
        
        initial_token_price = st.number_input(
            "Initial Token Price (USD)",
            min_value=0.01,
            value=1.00,
            step=0.01
        )
        
        monthly_price_appreciation = st.number_input(
            "Monthly Price Appreciation %",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.1
        )
    
    with col2:
        st.markdown("### **💰 Investment Settings**")
        
        projection_months = st.number_input(
            "Projection Period (Months)",
            min_value=6,
            max_value=60,
            value=36,
            step=6
        )
        
        target_roi = st.number_input(
            "Target ROI %",
            min_value=0.0,
            max_value=1000.0,
            value=200.0,
            step=10.0
        )
        
        investment_amount = st.number_input(
            "Investment Amount (USD)",
            min_value=100.0,
            value=10000.0,
            step=100.0
        )
        
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["Conservative", "Moderate", "Aggressive"],
            index=1
        )
    
    # Generate projections
    months = list(range(projection_months + 1))
    users_projection = []
    price_projection = []
    value_projection = []
    investment_projection = []
    
    current_users = initial_users
    current_price = initial_token_price
    
    for month in months:
        users_projection.append(current_users)
        price_projection.append(current_price)
        
        # Calculate monthly platform value
        daily_content = current_users * 0.1  # 10% create content daily
        daily_views = daily_content * 500  # 500 views per content avg
        daily_engagement_rate = 12.0  # 12% engagement
        
        daily_interactions = daily_views * (1 + (daily_engagement_rate/100) * 1.5)  # Simplified
        monthly_community_value = daily_interactions * 30 * 0.50  # $0.50 per interaction
        
        # Investment attraction
        monthly_investment = monthly_community_value * 50 * 0.85 * 0.75  # Efficiency factors
        
        value_projection.append(monthly_community_value)
        investment_projection.append(monthly_investment)
        
        # Update for next month
        if month < projection_months:
            current_users *= (1 + monthly_growth_rate / 100)
            current_price *= (1 + monthly_price_appreciation / 100)
    
    # Investment analysis
    final_price = price_projection[-1]
    initial_tokens = investment_amount / initial_token_price
    final_value = initial_tokens * final_price
    total_roi = ((final_value - investment_amount) / investment_amount) * 100
    
    # Results
    st.markdown("---")
    st.markdown("## 📊 **Investment Projections**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Final Users", f"{users_projection[-1]:,.0f}", f"+{((users_projection[-1]/users_projection[0]-1)*100):,.0f}%")
    
    with col2:
        st.metric("💰 Final Token Price", f"${final_price:.2f}", f"+{((final_price/initial_token_price-1)*100):,.0f}%")
    
    with col3:
        st.metric("📈 Investment ROI", f"{total_roi:,.0f}%", f"Target: {target_roi:.0f}%")
    
    with col4:
        final_investment_value = final_value
        st.metric("💎 Final Investment Value", f"${final_investment_value:,.2f}", f"${final_investment_value-investment_amount:,.2f}")
    
    # Charts
    st.markdown("### **📈 Growth Projections**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_safe_chart(months, users_projection, "User Growth", "line")
    
    with col2:
        create_safe_chart(months, price_projection, "Token Price Growth", "line")
    
    # Investment recommendation
    st.markdown("### **💡 Investment Recommendation**")
    
    if total_roi >= target_roi:
        recommendation = "🟢 **STRONG BUY** - Projected ROI exceeds target"
        color = "success"
    elif total_roi >= target_roi * 0.7:
        recommendation = "🟡 **MODERATE BUY** - Projected ROI close to target"
        color = "warning"
    else:
        recommendation = "🔴 **HOLD/REVIEW** - Projected ROI below target"
        color = "error"
    
    if color == "success":
        st.success(recommendation)
    elif color == "warning":
        st.warning(recommendation)
    else:
        st.error(recommendation)
    
    # Risk analysis
    risk_factors = {
        "Conservative": 0.7,
        "Moderate": 1.0,
        "Aggressive": 1.3
    }
    
    risk_multiplier = risk_factors[risk_tolerance]
    adjusted_roi = total_roi * risk_multiplier
    
    st.markdown(f"""
    **Risk-Adjusted Analysis ({risk_tolerance}):**
    - Base ROI: {total_roi:.0f}%
    - Risk Multiplier: {risk_multiplier}x
    - Adjusted ROI: {adjusted_roi:.0f}%
    - Break-even Time: ~{projection_months//2} months (estimated)
    """)
    
    return {
        'total_roi': total_roi,
        'final_price': final_price,
        'final_users': users_projection[-1],
        'recommendation': recommendation
    }

def export_functionality(data_dict):
    """Export functionality for all analyses"""
    
    st.markdown("---")
    st.markdown("## 📊 **Export Analysis**")
    
    # Combine all data
    export_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        **data_dict
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON export
        json_data = json.dumps(export_data, indent=2, default=str)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"vcoin_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
    
    with col2:
        # Text report
        report = f"""
VCOIN V4 Unified Analysis Report
Generated: {export_data['timestamp']}

SUMMARY:
{json.dumps(export_data, indent=2, default=str)}

This comprehensive analysis covers educational learning,
content calculations, creator-consumer balance, and
investment projections for the VCOIN V4 platform.
        """
        
        st.download_button(
            label="📄 Download Report",
            data=report,
            file_name=f"vcoin_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

def main():
    """Main unified application"""
    
    # Page configuration
    st.set_page_config(
        page_title="VCOIN V4 Unified Platform",
        page_icon="💎",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize dependencies
    if 'dependencies' not in st.session_state:
        st.session_state.dependencies = safe_import_check()
    
    deps = st.session_state.dependencies
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .tab-content {
        padding: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
    <h1>💎 VCOIN V4 Unified Platform</h1>
    <p>Complete tokenomics analysis in one application</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dependency status
    if not all(v for v in deps.values() if v is not None):
        st.warning("""
        ⚠️ **Running in Safe Mode** - Some optional features disabled due to dependency issues.
        All core calculations remain fully functional!
        """)
    else:
        st.success("✅ **Full Mode** - All features available!")
    
    # Main navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎓 Learn Tokenomics", 
        "🎬 Content Calculator", 
        "⚖️ Platform Balance", 
        "💎 Investment Analysis"
    ])
    
    # Store results for export
    all_results = {}
    
    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        educational_results = educational_interface()
        all_results.update({"educational": educational_results})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        content_results = content_calculator_interface()
        all_results.update({"content": content_results})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        balance_results = creator_consumer_balance_interface()
        all_results.update({"balance": balance_results})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        investment_results = investment_analysis_interface()
        all_results.update({"investment": investment_results})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export functionality (always visible)
    export_functionality(all_results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>VCOIN V4 Unified Platform</strong></p>
    <p>🎓 Learn • 🎬 Calculate • ⚖️ Balance • 💎 Invest</p>
    <p><em>Single command deployment: <code>streamlit run vcoin_unified.py</code></em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
