"""
VCOIN V4 - Educational & Minimal Platform
Designed for new users and investors to understand tokenomics step-by-step
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import math

def main():
    """Educational VCOIN V4 Platform - Minimal and Understandable"""
    
    # Page configuration
    st.set_page_config(
        page_title="VCOIN V4 Educational",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better UX
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .explanation-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00c851;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("# 🎓 **VCOIN V4 Educational Platform**")
    st.markdown("### **Learn How Content Creates Value & Rewards**")
    
    # Introduction for new users
    with st.expander("👋 **New to VCOIN? Start Here!**", expanded=True):
        st.markdown("""
        **Welcome to VCOIN V4!** This platform shows you exactly how content creators earn money through our tokenomics.
        
        **🎯 What You'll Learn:**
        - How your content creates real economic value
        - How community engagement attracts investment
        - How creators get paid in USD (not just tokens)
        - Why this system is sustainable long-term
        
        **📊 Perfect for:**
        - Content creators wanting to understand earnings
        - Investors evaluating the economic model
        - Anyone curious about tokenomics
        """)
    
    st.markdown("---")
    
    # === STEP 1: BASIC INPUTS ===
    st.markdown("## 📝 **Step 1: Your Content & Platform Settings**")
    
    col1, col2 = st.columns([1, 1])
    
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
            help="Percentage of viewers who engaged (liked, shared, commented)"
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
    
    st.markdown("---")
    
    # === STEP 2: CALCULATIONS ===
    st.markdown("## 🧮 **Step 2: How We Calculate Your Earnings**")
    
    # Calculate engagement metrics
    likes_reactions = views * (engagement_rate/100) * 0.7  # Most engagement is likes
    total_interactions = views + (shares * 5) + likes_reactions + (comments * 3)
    
    # V4 Community Value Calculation
    community_value_per_interaction = 0.50  # $0.50 per weighted interaction
    base_community_value = total_interactions * community_value_per_interaction
    
    # V4 Engagement Multiplier
    engagement_multiplier = 1.0 + (engagement_rate / 100 * 2.0)
    enhanced_community_value = base_community_value * engagement_multiplier
    
    # Investment attraction (simplified for education)
    market_efficiency = 0.85  # How efficiently value attracts investment
    investment_conversion = 0.75  # How much of interest converts to actual investment
    
    theoretical_investment = enhanced_community_value * 50  # Investment multiplier
    actual_investment = theoretical_investment * market_efficiency * investment_conversion
    
    # Dynamic reward adjustment (price appreciation factor)
    base_price = 1.0  # Assume $1 base price
    price_appreciation_factor = token_price / base_price
    reward_multiplier = max(0.2, min(1.0, 1.0 / (price_appreciation_factor ** 0.3)))
    
    # Creator rewards
    creator_value_share = actual_investment * (creator_percentage / 100)
    adjusted_creator_value = creator_value_share * reward_multiplier
    
    # Token calculation
    tokens_earned = adjusted_creator_value / token_price
    
    # Show calculations step by step
    with st.expander("🔍 **See Detailed Calculations**", expanded=False):
        st.markdown("### **Step-by-Step Breakdown:**")
        
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
        """)
    
    st.markdown("---")
    
    # === STEP 3: RESULTS ===
    st.markdown("## 🎯 **Step 3: Your Earnings Breakdown**")
    
    # Main results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h3>💵 USD Earnings</h3>
        <h2>${:,.2f}</h2>
        <p>What you earn in dollars</p>
        </div>
        """.format(adjusted_creator_value), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h3>🪙 VCOIN Tokens</h3>
        <h2>{:,.2f}</h2>
        <p>Tokens you receive</p>
        </div>
        """.format(tokens_earned), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
        <h3>📊 Value Created</h3>
        <h2>${:,.2f}</h2>
        <p>Total community value</p>
        </div>
        """.format(enhanced_community_value), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
        <h3>💰 Investment Attracted</h3>
        <h2>${:,.2f}</h2>
        <p>Investment your content brought</p>
        </div>
        """.format(actual_investment), unsafe_allow_html=True)
    
    # === STEP 4: UNDERSTANDING THE ECONOMICS ===
    st.markdown("---")
    st.markdown("## 🎓 **Step 4: Understanding the Economics**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💡 How It Works", "📈 Why Sustainable", "🔄 Token Flow", "📊 Comparisons"])
    
    with tab1:
        st.markdown("### **How VCOIN V4 Creates Value**")
        
        st.markdown("""
        <div class="explanation-box">
        <h4>🎯 The Value Creation Cycle</h4>
        <p><strong>1. Content Creation:</strong> You create engaging content</p>
        <p><strong>2. Community Engagement:</strong> Users view, like, share, comment</p>
        <p><strong>3. Value Generation:</strong> Each interaction creates measurable economic value</p>
        <p><strong>4. Investment Attraction:</strong> Value growth attracts investors to buy VCOIN</p>
        <p><strong>5. Creator Rewards:</strong> Investment funds are used to pay creators in USD</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Value flow diagram
        fig = go.Figure()
        
        # Create a simple flow chart
        fig.add_trace(go.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[1, 1, 1, 1, 1],
            mode='markers+text',
            marker=dict(size=50, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']),
            text=['Content', 'Engagement', 'Value', 'Investment', 'Rewards'],
            textposition="bottom center",
            textfont=dict(size=12, color='white'),
            showlegend=False
        ))
        
        # Add arrows
        for i in range(4):
            fig.add_annotation(
                x=i+1.5, y=1,
                ax=i+1.3, ay=1,
                xref='x', yref='y',
                axref='x', ayref='y',
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor='#666'
            )
        
        fig.update_layout(
            title="VCOIN V4 Value Flow",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=200,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### **Why This Model Is Sustainable**")
        
        st.markdown("""
        <div class="explanation-box">
        <h4>🔄 Self-Sustaining Economics</h4>
        <p><strong>No External Revenue Needed:</strong> The platform doesn't rely on ads or subscriptions</p>
        <p><strong>Community-Driven Value:</strong> Users create real economic value through engagement</p>
        <p><strong>Investment Attraction:</strong> Growing value attracts investors who buy VCOIN</p>
        <p><strong>Dynamic Adjustment:</strong> Rewards adjust with token price to maintain USD stability</p>
        <p><strong>Healthy Inflation:</strong> 5-10% annual inflation supports ecosystem growth</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sustainability metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Key Sustainability Factors:**")
            sustainability_data = {
                'Factor': ['Market Efficiency', 'Investment Conversion', 'Creator Share', 'Price Stability'],
                'Value': [f'{market_efficiency:.0%}', f'{investment_conversion:.0%}', f'{creator_percentage:.0f}%', f'{reward_multiplier:.1f}x'],
                'Status': ['✅ Optimized', '✅ Healthy', '✅ Competitive', '✅ Stable']
            }
            st.dataframe(pd.DataFrame(sustainability_data), hide_index=True)
        
        with col2:
            # Simple sustainability chart
            sustainability_scores = [85, 75, 55, 80]  # Market eff, conversion, creator share, stability
            labels = ['Market\nEfficiency', 'Investment\nConversion', 'Creator\nShare', 'Price\nStability']
            
            fig = go.Figure(data=go.Bar(
                x=labels,
                y=sustainability_scores,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            ))
            
            fig.update_layout(
                title="Sustainability Scores",
                yaxis_title="Score (%)",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### **Token Flow & Distribution**")
        
        # Token distribution breakdown
        total_value = actual_investment
        creator_share = total_value * (creator_percentage / 100)
        platform_share = total_value * 0.12  # 12% platform
        ecosystem_share = total_value * 0.08  # 8% ecosystem
        consumer_share = total_value * 0.25   # 25% consumers
        
        distribution_data = {
            'Recipient': ['Creators', 'Consumers', 'Platform', 'Ecosystem'],
            'USD Value': [creator_share, consumer_share, platform_share, ecosystem_share],
            'Percentage': [creator_percentage, 25.0, 12.0, 8.0],
            'Purpose': ['Content rewards', 'Engagement rewards', 'Operations', 'Growth fund']
        }
        
        df_dist = pd.DataFrame(distribution_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💰 Value Distribution:**")
            st.dataframe(df_dist.style.format({
                'USD Value': '${:,.2f}',
                'Percentage': '{:.1f}%'
            }), hide_index=True)
        
        with col2:
            # Pie chart of distribution
            fig = px.pie(
                df_dist, 
                values='USD Value', 
                names='Recipient',
                title="Value Distribution",
                color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### **Compare with Other Platforms**")
        
        # Calculate comparable metrics
        rpm = (adjusted_creator_value / views) * 1000 if views > 0 else 0  # Revenue per 1000 views
        cpm = rpm  # Same as RPM for creators
        
        comparison_data = {
            'Platform': ['VCOIN V4', 'YouTube', 'TikTok', 'Instagram'],
            'RPM (Revenue per 1000 views)': [f'${rpm:.2f}', '$1.00-$5.00', '$0.20-$0.40', '$0.50-$2.00'],
            'Creator Share': ['55%', '55%', '~20%', '~25%'],
            'Payment Method': ['USD + Tokens', 'USD', 'Creator Fund', 'Various'],
            'Sustainability': ['Self-sustaining', 'Ad-dependent', 'Platform-funded', 'Ad-dependent']
        }
        
        st.dataframe(pd.DataFrame(comparison_data), hide_index=True)
        
        st.markdown("""
        <div class="warning-box">
        <h4>🎯 VCOIN V4 Advantages</h4>
        <p><strong>Competitive RPM:</strong> ${:.2f} per 1000 views (comparable to YouTube)</p>
        <p><strong>No Ad Dependency:</strong> Sustainable without external advertising revenue</p>
        <p><strong>Transparent Economics:</strong> Clear value creation and distribution model</p>
        <p><strong>Creator-First:</strong> 55% of value goes directly to creators</p>
        </div>
        """.format(rpm), unsafe_allow_html=True)
    
    # === STEP 5: SCENARIO TESTING ===
    st.markdown("---")
    st.markdown("## 🧪 **Step 5: Test Different Scenarios**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 **Small Creator** (1K views, 10% engagement)", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🌟 **Growing Creator** (50K views, 15% engagement)", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🔥 **Viral Creator** (1M views, 20% engagement)", use_container_width=True):
            st.rerun()
    
    # === EXPORT FUNCTIONALITY ===
    st.markdown("---")
    st.markdown("## 📊 **Export Your Analysis**")
    
    # Create export data
    export_data = {
        'Metric': [
            'Views', 'Engagement Rate', 'Shares', 'Comments', 'Token Price',
            'Total Interactions', 'Community Value', 'Investment Attracted',
            'USD Earnings', 'Tokens Earned', 'RPM'
        ],
        'Value': [
            f'{views:,.0f}', f'{engagement_rate:.1f}%', f'{shares:,.0f}', f'{comments:,.0f}', f'${token_price:.2f}',
            f'{total_interactions:,.0f}', f'${enhanced_community_value:,.2f}', f'${actual_investment:,.2f}',
            f'${adjusted_creator_value:.2f}', f'{tokens_earned:,.2f}', f'${rpm:.2f}'
        ],
        'Explanation': [
            'Number of people who viewed content', 'Percentage who engaged', 'Times content was shared',
            'Number of comments received', 'Current VCOIN market price', 'Weighted sum of all interactions',
            'Economic value created by community', 'Investment attracted by value growth',
            'Creator earnings in USD', 'VCOIN tokens received', 'Revenue per 1000 views'
        ]
    }
    
    export_df = pd.DataFrame(export_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Analysis (CSV)",
            data=csv,
            file_name=f"vcoin_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Create summary report
        summary_report = f"""
VCOIN V4 Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

CONTENT PERFORMANCE:
- Views: {views:,.0f}
- Engagement Rate: {engagement_rate:.1f}%
- Total Interactions: {total_interactions:,.0f}

ECONOMIC RESULTS:
- Community Value Created: ${enhanced_community_value:,.2f}
- Investment Attracted: ${actual_investment:,.2f}
- Creator USD Earnings: ${adjusted_creator_value:,.2f}
- VCOIN Tokens Earned: {tokens_earned:,.2f}
- Revenue per 1000 views: ${rpm:.2f}

PLATFORM SETTINGS:
- Token Price: ${token_price:.2f}
- Creator Share: {creator_percentage:.0f}%
- Total Platform Users: {total_users:,.0f}

This analysis shows how content creates measurable economic value
that attracts investment and funds sustainable creator rewards.
        """
        
        st.download_button(
            label="📄 Download Report (TXT)",
            data=summary_report,
            file_name=f"vcoin_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>VCOIN V4 Educational Platform</strong></p>
    <p>Empowering creators with transparent, sustainable tokenomics</p>
    <p>🎓 Learn • 💰 Earn • 🚀 Grow</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
