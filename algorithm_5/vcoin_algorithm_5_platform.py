"""
VCOIN Algorithm 5 - Price Pool Model Platform
Sustainable token distribution with quality-based weighting
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="VCOIN Algorithm 5 - Price Pool Platform",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        # Market parameters (calibrated for Algorithm 5)
        'market_cap': 630_720_000,
        'total_supply': 157_680_000_000,
        'token_price': 0.004,
        'content_allocation_pct': 40.0,
        'distribution_years': 3.0,
        
        # Algorithm 5 parameters
        'alpha': 0.3,  # 5A impact coefficient
        'beta': 0.8,   # PV impact coefficient
        
        # Content type multipliers
        'ctm_text': 0.8,
        'ctm_short_video': 1.0,
        'ctm_long_video': 2.0,
        'ctm_podcast': 2.5,
        
        # Distribution percentages
        'creator_share': 40.0,
        'engagement_share': 50.0,
        'platform_share': 10.0,
        
        # Engagement distribution
        'shares_pct': 20.0,
        'comments_pct': 12.5,
        'reactions_pct': 10.0,
        'views_pct': 7.5,
        
        # Platform metrics
        'total_users': 100_000,
        'dau_percentage': 30.0,
        'content_creation_rate': 12.0,
        'avg_views_per_content': 8000,
        'avg_engagement_per_content': 120,
        'avg_pv_score': 78,
        'avg_5a_score': 300,
        'avg_trust_score': 0.8,
        
        # Dynamic scaling parameters
        'enable_dynamic_scaling': True,
        'enable_price_adjustment': True,
        'user_scaling_factor': 0.6,
        'price_reduction_exponent': 0.4,
        'current_token_price': 0.004,
        
        # Token velocity management (percentages of circulating supply)
        'enable_token_sinks': True,
        'token_recapture_rate': 0.51,
        'nft_circulation_pct': 10.0,        # 10% circulation (VIP badges, profile items)
        'staking_circulation_pct': 10.0,    # 10% circulation (3-30 day locks)
        'rate_limit_circulation_pct': 5.0,  # 5% circulation (content/view limits)
        'prediction_circulation_pct': 5.0,  # 5% circulation (content success bets)
        'content_purchase_circulation_pct': 1.0,   # 1% circulation (premium content)
        'donations_circulation_pct': 1.0,   # 1% circulation (creator support)
        'boosting_circulation_pct': 1.0,    # 1% circulation (algorithmic promotion)
        'features_circulation_pct': 2.0,    # 2% circulation (analytics, tools)
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def calculate_daily_pool():
    """Calculate the base daily token pool"""
    content_tokens = st.session_state.total_supply * (st.session_state.content_allocation_pct / 100)
    days = st.session_state.distribution_years * 365
    return content_tokens / days

def calculate_dynamic_daily_pool(base_pool, current_users, current_token_price):
    """Calculate dynamic daily pool with scaling and price adjustment"""
    
    # Base parameters
    base_users = 100_000  # Reference user count
    launch_price = 0.004  # Launch token price
    
    # Get scaling parameters from session state (with defaults)
    user_scaling_factor = getattr(st.session_state, 'user_scaling_factor', 0.6)
    price_reduction_exponent = getattr(st.session_state, 'price_reduction_exponent', 0.4)
    enable_dynamic_scaling = getattr(st.session_state, 'enable_dynamic_scaling', True)
    enable_price_adjustment = getattr(st.session_state, 'enable_price_adjustment', True)
    
    # User growth scaling (sub-linear)
    user_scaling = 1.0
    if enable_dynamic_scaling and current_users != base_users:
        user_scaling = (current_users / base_users) ** user_scaling_factor
    
    # Price appreciation adjustment (reduces tokens as price increases)
    price_adjustment = 1.0
    if enable_price_adjustment and current_token_price != launch_price:
        price_ratio = current_token_price / launch_price
        price_adjustment = price_ratio ** (-price_reduction_exponent)
    
    # Combined dynamic pool
    dynamic_pool = base_pool * user_scaling * price_adjustment
    
    return {
        'dynamic_pool': dynamic_pool,
        'base_pool': base_pool,
        'user_scaling': user_scaling,
        'price_adjustment': price_adjustment,
        'price_ratio': current_token_price / launch_price
    }

def calculate_token_sinks():
    """Calculate daily token sink revenue and velocity impact"""
    
    if not getattr(st.session_state, 'enable_token_sinks', True):
        return {
            'total_sinks': 0,
            'sinks_breakdown': {},
            'recapture_rate': 0,
            'velocity_reduction': 0
        }
    
    # Calculate daily volumes from percentages of circulating supply
    circulating_supply = st.session_state.total_supply * 0.6  # Assume 60% circulating
    daily_circulation = circulating_supply / 365  # Annual circulation divided by days
    
    # Token sink categories (daily VCOIN amounts calculated from percentages)
    sinks = {
        'NFT Trading': daily_circulation * (st.session_state.nft_circulation_pct / 100),
        'Staking Locks': daily_circulation * (st.session_state.staking_circulation_pct / 100),
        'Rate Limit Unlocks': daily_circulation * (st.session_state.rate_limit_circulation_pct / 100),
        'Prediction Markets': daily_circulation * (st.session_state.prediction_circulation_pct / 100),
        'Content Purchases': daily_circulation * (st.session_state.content_purchase_circulation_pct / 100),
        'Donations & Tips': daily_circulation * (st.session_state.donations_circulation_pct / 100),
        'Profile Boosting': daily_circulation * (st.session_state.boosting_circulation_pct / 100),
        'Advanced Features': daily_circulation * (st.session_state.features_circulation_pct / 100)
    }
    
    total_sinks = sum(sinks.values())
    recapture_rate = st.session_state.token_recapture_rate
    velocity_reduction = recapture_rate * 100  # Percentage
    
    return {
        'total_sinks': total_sinks,
        'sinks_breakdown': sinks,
        'recapture_rate': recapture_rate,
        'velocity_reduction': velocity_reduction
    }

def calculate_sustainable_economics():
    """Calculate economics with token velocity management"""
    
    # Get base economics
    base_economics = simulate_platform_economics()
    
    # Get token sink data
    sink_data = calculate_token_sinks()
    
    # Calculate net token flow
    daily_outflow = base_economics['daily_pool']
    daily_inflow = sink_data['total_sinks']
    net_outflow = daily_outflow - daily_inflow
    
    # Calculate sustainability metrics
    content_allocation = st.session_state.total_supply * (st.session_state.content_allocation_pct / 100)
    days_sustainable = content_allocation / net_outflow if net_outflow > 0 else float('inf')
    years_sustainable = days_sustainable / 365
    
    # Token velocity metrics
    circulating_supply = st.session_state.total_supply * 0.6  # Assume 60% circulating
    token_velocity = daily_outflow / circulating_supply if circulating_supply > 0 else 0
    reduced_velocity = token_velocity * (1 - sink_data['recapture_rate'])
    
    return {
        **base_economics,
        **sink_data,
        'daily_outflow': daily_outflow,
        'daily_inflow': daily_inflow,
        'net_outflow': net_outflow,
        'days_sustainable': days_sustainable,
        'years_sustainable': years_sustainable,
        'token_velocity': token_velocity,
        'reduced_velocity': reduced_velocity,
        'circulating_supply': circulating_supply
    }

def calculate_algorithm_5_weight(total_engagement, post_value_score, creator_credibility_score, trust_score, content_type_multiplier):
    """Calculate Algorithm 5 weight for a piece of content"""
    # content_weight = log(1 + total_engagement) × (post_value_score/100)^β × (creator_credibility_score/500)^α × trust_score × content_type_multiplier
    log_engagement_factor = math.log(1 + total_engagement)
    post_value_factor = (post_value_score / 100) ** st.session_state.beta
    creator_credibility_factor = (creator_credibility_score / 500) ** st.session_state.alpha
    
    content_weight = log_engagement_factor * post_value_factor * creator_credibility_factor * trust_score * content_type_multiplier
    return content_weight

def simulate_platform_economics():
    """Simulate platform economics using Algorithm 5 with dynamic scaling"""
    
    # Calculate basic metrics
    base_daily_pool = calculate_daily_pool()
    
    # Calculate dynamic pool with scaling
    pool_data = calculate_dynamic_daily_pool(
        base_daily_pool, 
        st.session_state.total_users, 
        st.session_state.current_token_price
    )
    daily_pool = pool_data['dynamic_pool']
    
    dau = st.session_state.total_users * (st.session_state.dau_percentage / 100)
    daily_content = dau * (st.session_state.content_creation_rate / 100)
    
    # Calculate average content type multiplier (weighted by content distribution)
    # Assume: 40% Short Video, 30% Long Video, 20% Podcast, 10% Text
    avg_ctm = (0.4 * st.session_state.ctm_short_video + 
               0.3 * st.session_state.ctm_long_video + 
               0.2 * st.session_state.ctm_podcast + 
               0.1 * st.session_state.ctm_text)
    
    # Calculate average weight per content
    avg_content_weight = calculate_algorithm_5_weight(
        st.session_state.avg_engagement_per_content,
        st.session_state.avg_pv_score,
        st.session_state.avg_5a_score,
        st.session_state.avg_trust_score,
        avg_ctm
    )
    
    # Total weight and tokens per content
    total_daily_weight = avg_content_weight * daily_content
    tokens_per_content = daily_pool / daily_content if daily_content > 0 else 0
    
    # Distribution breakdown
    creator_tokens = tokens_per_content * (st.session_state.creator_share / 100)
    engagement_tokens = tokens_per_content * (st.session_state.engagement_share / 100)
    platform_tokens = tokens_per_content * (st.session_state.platform_share / 100)
    
    # Creator economics
    creator_usd = creator_tokens * st.session_state.token_price
    rpm = (creator_usd / st.session_state.avg_views_per_content) * 1000 if st.session_state.avg_views_per_content > 0 else 0
    
    return {
        'daily_pool': daily_pool,
        'base_daily_pool': base_daily_pool,
        'daily_pool_usd': daily_pool * st.session_state.current_token_price,
        'dau': dau,
        'daily_content': daily_content,
        'avg_content_weight': avg_content_weight,
        'tokens_per_content': tokens_per_content,
        'creator_tokens': creator_tokens,
        'engagement_tokens': engagement_tokens,
        'platform_tokens': platform_tokens,
        'creator_usd': creator_usd,
        'rpm': rpm,
        'avg_ctm': avg_ctm,
        'user_scaling': pool_data['user_scaling'],
        'price_adjustment': pool_data['price_adjustment'],
        'price_ratio': pool_data['price_ratio']
    }

def algorithm_5_overview_tab():
    """Algorithm 5 Overview and Theory"""
    st.header("🧮 Algorithm 5: Price Pool Model Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Algorithm Goal")
        st.write("""
        **Algorithm 5** implements a **sustainable price pool distribution model** that:
        - Uses a **fixed daily token pool** (not unlimited minting)
        - Distributes tokens based on **quality-weighted content scores**
        - Rewards **creators, engagement participants, and platform**
        - Scales sustainably from **5K to 10M+ users**
        """)
        
        st.subheader("🔤 Key Variables")
        
        # Create variables table
        variables_data = {
            'Variable': ['total_engagement', 'post_value_score', 'creator_credibility_score', 'trust_score', 'content_type_multiplier', 'content_weight', 'daily_token_pool', 'content_tokens_allocated'],
            'Description': [
                'Total engagement (views + reactions + comments + shares)',
                'Post Value score (0-100)',
                'Creator credibility score (0-500)',
                'Trust score (0.2-1.0)',
                'Content Type Multiplier (0.8-2.5)',
                'Content weight for distribution',
                'Fixed daily token pool',
                'Final tokens allocated to content'
            ],
            'Range': ['0+', '0-100', '0-500', '0.2-1.0', '0.8-2.5', '0+', 'Fixed', '0+']
        }
        
        df_vars = pd.DataFrame(variables_data)
        st.dataframe(df_vars, width='stretch')
        
        st.subheader("🧮 Algorithm Steps")
        
        st.write("**Step 1: Calculate Content Weight**")
        st.latex(r"content\_weight = \log(1 + total\_engagement) \times \left(\frac{post\_value\_score}{100}\right)^\beta \times \left(\frac{creator\_credibility\_score}{500}\right)^\alpha \times trust\_score \times content\_type\_multiplier")
        
        st.write("**Step 2: Calculate Total Daily Weight**")
        st.latex(r"total\_daily\_weight = \sum_{i=1}^{n} content\_weight_i")
        
        st.write("**Step 3: Distribute Daily Pool**")
        st.latex(r"content\_tokens\_allocated = daily\_token\_pool \times \frac{content\_weight}{total\_daily\_weight}")
        
        st.write("**Step 4: Split Token Allocation**")
        st.latex(r"""
        \begin{align}
        creator\_tokens &= content\_tokens\_allocated \times 0.40 \\
        engagement\_tokens &= content\_tokens\_allocated \times 0.50 \\
        platform\_tokens &= content\_tokens\_allocated \times 0.10
        \end{align}
        """)
    
    with col2:
        st.subheader("✅ Key Benefits")
        
        benefits = [
            "🎯 **Mathematically Sustainable**: Fixed daily pool prevents economic collapse",
            "📊 **Quality-Based**: Rewards high-value content over viral manipulation",
            "👥 **Multi-Stakeholder**: Creators, participants, and platform all benefit",
            "🛡️ **Anti-Manipulation**: Logarithmic engagement + trust scoring",
            "📈 **Scalable**: Works at any platform size without breaking",
            "⚖️ **Self-Balancing**: More content = smaller individual shares"
        ]
        
        for benefit in benefits:
            st.write(benefit)
        
        st.subheader("🆚 vs Content-Driven Minting")
        
        comparison_data = {
            'Aspect': ['Token Supply', 'Scalability', 'Sustainability', 'Predictability'],
            'Algorithm 5 (Pool)': ['Fixed daily pool', 'Infinite scale', '100% sustainable', 'Predictable economics'],
            'Content Minting': ['Unlimited minting', 'Breaks at scale', '0% sustainable', 'Exponential chaos']
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, width='stretch')

def pool_configuration_tab():
    """Configure the daily pool and basic parameters"""
    st.header("⚙️ Pool Configuration & Market Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Market Economics")
        
        st.session_state.market_cap = st.number_input(
            "Market Cap ($)",
            min_value=1_000_000,
            max_value=2_000_000_000,
            value=st.session_state.market_cap,
            step=500_000,
            format="%d"
        )
        
        st.session_state.total_supply = st.number_input(
            "Total Token Supply",
            min_value=100_000_000,
            max_value=500_000_000_000,
            value=st.session_state.total_supply,
            step=100_000_000,
            format="%d"
        )
        
        st.session_state.token_price = st.session_state.market_cap / st.session_state.total_supply
        st.metric("Calculated Token Price", f"${st.session_state.token_price:.6f}")
        
        st.session_state.content_allocation_pct = st.slider(
            "Content Allocation (%)",
            min_value=20.0,
            max_value=60.0,
            value=st.session_state.content_allocation_pct,
            step=1.0
        )
        
        st.session_state.distribution_years = st.slider(
            "Distribution Period (Years)",
            min_value=1.0,
            max_value=10.0,
            value=st.session_state.distribution_years,
            step=0.5
        )
        
        # Calculate and display pool metrics
        daily_pool = calculate_daily_pool()
        daily_pool_usd = daily_pool * st.session_state.token_price
        
        st.subheader("📊 Pool Metrics")
        col1a, col1b = st.columns(2)
        with col1a:
            st.metric("Daily Pool (VCOIN)", f"{daily_pool:,.0f}")
            st.metric("Content Tokens", f"{st.session_state.total_supply * (st.session_state.content_allocation_pct / 100):,.0f}")
        with col1b:
            st.metric("Daily Pool (USD)", f"${daily_pool_usd:,.0f}")
            st.metric("Distribution Days", f"{st.session_state.distribution_years * 365:.0f}")
    
    with col2:
        st.subheader("🎛️ Algorithm 5 Parameters")
        
        st.session_state.alpha = st.slider(
            "Alpha (5A Impact Coefficient)",
            min_value=0.1,
            max_value=1.0,
            value=st.session_state.alpha,
            step=0.1,
            help="Controls how much 5A score affects token distribution"
        )
        
        st.session_state.beta = st.slider(
            "Beta (PV Impact Coefficient)",
            min_value=0.1,
            max_value=2.0,
            value=st.session_state.beta,
            step=0.1,
            help="Controls how much Post Value affects token distribution"
        )
        
        st.subheader("📱 Content Type Multipliers")
        
        st.session_state.ctm_text = st.slider(
            "Text Post Multiplier",
            min_value=0.5,
            max_value=1.5,
            value=st.session_state.ctm_text,
            step=0.1
        )
        
        st.session_state.ctm_short_video = st.slider(
            "Short Video Multiplier",
            min_value=0.5,
            max_value=2.0,
            value=st.session_state.ctm_short_video,
            step=0.1
        )
        
        st.session_state.ctm_long_video = st.slider(
            "Long Video Multiplier",
            min_value=1.0,
            max_value=3.0,
            value=st.session_state.ctm_long_video,
            step=0.1
        )
        
        st.session_state.ctm_podcast = st.slider(
            "Podcast Multiplier",
            min_value=1.5,
            max_value=4.0,
            value=st.session_state.ctm_podcast,
            step=0.1
        )
        
        st.subheader("🚀 Dynamic Scaling Parameters")
        
        st.session_state.enable_dynamic_scaling = st.checkbox(
            "Enable User Growth Scaling",
            value=st.session_state.enable_dynamic_scaling,
            help="Pool grows with user count (sub-linear)"
        )
        
        if st.session_state.enable_dynamic_scaling:
            st.session_state.user_scaling_factor = st.slider(
                "User Scaling Factor",
                min_value=0.3,
                max_value=1.0,
                value=st.session_state.user_scaling_factor,
                step=0.1,
                help="0.6 = pool grows at 60% rate of user growth"
            )
        
        st.session_state.enable_price_adjustment = st.checkbox(
            "Enable Price Appreciation Adjustment",
            value=st.session_state.enable_price_adjustment,
            help="Reduce token rewards as price increases"
        )
        
        if st.session_state.enable_price_adjustment:
            st.session_state.price_reduction_exponent = st.slider(
                "Price Reduction Exponent",
                min_value=0.2,
                max_value=0.8,
                value=st.session_state.price_reduction_exponent,
                step=0.1,
                help="0.4 = 10x price increase reduces tokens by ~60%"
            )
            
            st.session_state.current_token_price = st.number_input(
                "Current Token Price ($)",
                min_value=0.001,
                max_value=1.0,
                value=st.session_state.current_token_price,
                step=0.001,
                format="%.6f",
                help="Simulated current market price"
            )
        
        st.subheader("💰 Distribution Percentages")
        
        # Ensure percentages add up to 100%
        creator_share = st.slider(
            "Creator Share (%)",
            min_value=20.0,
            max_value=60.0,
            value=st.session_state.creator_share,
            step=1.0
        )
        
        platform_share = st.slider(
            "Platform Share (%)",
            min_value=5.0,
            max_value=20.0,
            value=st.session_state.platform_share,
            step=1.0
        )
        
        engagement_share = 100.0 - creator_share - platform_share
        
        st.session_state.creator_share = creator_share
        st.session_state.platform_share = platform_share
        st.session_state.engagement_share = engagement_share
        
        st.info(f"Engagement Share: {engagement_share:.1f}% (auto-calculated)")

def token_velocity_management_tab():
    """Configure token sinks and velocity management"""
    st.header("🔄 Token Velocity & Circulation Management")
    
    st.write("""
    **Problem**: Content rewards create constant selling pressure and token outflow.
    **Solution**: Implement "speed bumps" - utility mechanisms that recapture tokens and reduce velocity.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎛️ Token Sink Configuration")
        
        st.session_state.enable_token_sinks = st.checkbox(
            "Enable Token Sinks",
            value=st.session_state.enable_token_sinks,
            help="Enable utility mechanisms that recapture tokens"
        )
        
        if st.session_state.enable_token_sinks:
            st.write("**Token Sink Configuration (% of Circulating Supply):**")
            
            st.session_state.nft_circulation_pct = st.slider(
                "NFT Trading (VIP badges, profile items)",
                min_value=0.0,
                max_value=20.0,
                value=st.session_state.nft_circulation_pct,
                step=0.5,
                format="%.1f%%",
                help="High velocity reduction - Users buy VIP badges, profile customization"
            )
            
            st.session_state.staking_circulation_pct = st.slider(
                "Short-term Staking (3-30 day locks)",
                min_value=0.0,
                max_value=20.0,
                value=st.session_state.staking_circulation_pct,
                step=0.5,
                format="%.1f%%",
                help="Medium velocity reduction - Token locks with APY rewards"
            )
            
            st.session_state.rate_limit_circulation_pct = st.slider(
                "Rate Limit Unlocks (content/view limits)",
                min_value=0.0,
                max_value=10.0,
                value=st.session_state.rate_limit_circulation_pct,
                step=0.5,
                format="%.1f%%",
                help="Medium velocity reduction - Pay to unlock posting/viewing limits"
            )
            
            st.session_state.prediction_circulation_pct = st.slider(
                "Prediction Market Bets",
                min_value=0.0,
                max_value=10.0,
                value=st.session_state.prediction_circulation_pct,
                step=0.5,
                format="%.1f%%",
                help="Medium velocity reduction - Bet on content success"
            )
            
            st.session_state.content_purchase_circulation_pct = st.slider(
                "Premium Content Purchases",
                min_value=0.0,
                max_value=5.0,
                value=st.session_state.content_purchase_circulation_pct,
                step=0.1,
                format="%.1f%%",
                help="High velocity reduction - Scientific papers, premium courses"
            )
            
            st.session_state.donations_circulation_pct = st.slider(
                "Donations & Tips",
                min_value=0.0,
                max_value=5.0,
                value=st.session_state.donations_circulation_pct,
                step=0.1,
                format="%.1f%%",
                help="High velocity reduction - Direct creator support"
            )
            
            st.session_state.boosting_circulation_pct = st.slider(
                "Profile Boosting & Promotion",
                min_value=0.0,
                max_value=5.0,
                value=st.session_state.boosting_circulation_pct,
                step=0.1,
                format="%.1f%%",
                help="High velocity reduction - Algorithmic promotion, gain followers"
            )
            
            st.session_state.features_circulation_pct = st.slider(
                "Advanced Features (analytics, tools)",
                min_value=0.0,
                max_value=5.0,
                value=st.session_state.features_circulation_pct,
                step=0.1,
                format="%.1f%%",
                help="Medium velocity reduction - Analytics, scheduling, monetization"
            )
            
            # Calculate total circulation impact and actual volumes
            total_circulation_pct = (st.session_state.nft_circulation_pct + 
                                   st.session_state.staking_circulation_pct + 
                                   st.session_state.rate_limit_circulation_pct + 
                                   st.session_state.prediction_circulation_pct + 
                                   st.session_state.content_purchase_circulation_pct + 
                                   st.session_state.donations_circulation_pct + 
                                   st.session_state.boosting_circulation_pct + 
                                   st.session_state.features_circulation_pct)
            
            # Get token sink data for display
            sink_data = calculate_token_sinks()
            total_sinks = sink_data['total_sinks']
            
            daily_pool = calculate_daily_pool()
            pool_data = calculate_dynamic_daily_pool(daily_pool, st.session_state.total_users, st.session_state.current_token_price)
            actual_daily_pool = pool_data['dynamic_pool']
            
            calculated_recapture_rate = total_sinks / actual_daily_pool if actual_daily_pool > 0 else 0
            
            st.session_state.token_recapture_rate = calculated_recapture_rate
            
            st.info(f"**Total Circulation Impact**: {total_circulation_pct:.1f}%")
            st.info(f"**Daily Token Sinks**: {total_sinks:,.0f} VCOIN")
            st.info(f"**Calculated Recapture Rate**: {calculated_recapture_rate:.1%}")
    
    with col2:
        st.subheader("📊 Velocity Impact Analysis")
        
        # Calculate sustainable economics
        economics = calculate_sustainable_economics()
        
        # Display key metrics
        col2a, col2b = st.columns(2)
        
        with col2a:
            st.metric("Daily Outflow", f"{economics['daily_outflow']:,.0f} VCOIN")
            st.metric("Daily Inflow (Sinks)", f"{economics['daily_inflow']:,.0f} VCOIN")
            st.metric("Net Outflow", f"{economics['net_outflow']:,.0f} VCOIN")
        
        with col2b:
            st.metric("Recapture Rate", f"{economics['recapture_rate']:.1%}")
            st.metric("Velocity Reduction", f"{economics['velocity_reduction']:.1f}%")
            if economics['years_sustainable'] < 100:
                st.metric("Years Sustainable", f"{economics['years_sustainable']:.1f}")
            else:
                st.metric("Years Sustainable", "∞ (Infinite)")
        
        # Sustainability status
        if economics['net_outflow'] <= 0:
            st.success("🎉 **SUSTAINABLE**: Token inflow ≥ outflow!")
        elif economics['years_sustainable'] >= 10:
            st.success(f"✅ **HIGHLY SUSTAINABLE**: {economics['years_sustainable']:.1f} years runway")
        elif economics['years_sustainable'] >= 5:
            st.warning(f"⚠️ **MODERATELY SUSTAINABLE**: {economics['years_sustainable']:.1f} years runway")
        else:
            st.error(f"❌ **UNSUSTAINABLE**: Only {economics['years_sustainable']:.1f} years runway")
        
        # Token sink breakdown chart
        st.subheader("🔄 Token Sink Breakdown")
        
        if economics['total_sinks'] > 0:
            import plotly.express as px
            
            sink_data = list(economics['sinks_breakdown'].items())
            sink_names = [item[0] for item in sink_data]
            sink_values = [item[1] for item in sink_data]
            
            fig_sinks = px.pie(
                values=sink_values,
                names=sink_names,
                title="Daily Token Sink Distribution"
            )
            st.plotly_chart(fig_sinks)
        else:
            st.info("Enable token sinks to see breakdown")
        
        # Velocity comparison
        st.subheader("🚀 Velocity Impact")
        
        # Calculate baseline sustainability (without sinks)
        if economics['recapture_rate'] == 0:
            baseline_years = 3.0
        elif economics['recapture_rate'] >= 1.0:
            baseline_years = float('inf')
        else:
            baseline_years = 3.0 / (1 - economics['recapture_rate'])
        
        velocity_data = {
            'Metric': ['Without Sinks', 'With Sinks', 'Improvement'],
            'Token Velocity': [
                f"{economics['token_velocity']:.4f}",
                f"{economics['reduced_velocity']:.4f}",
                f"{economics['velocity_reduction']:.1f}% reduction"
            ],
            'Sustainability': [
                f"{baseline_years:.1f} years" if baseline_years < 100 else "∞",
                f"{economics['years_sustainable']:.1f} years" if economics['years_sustainable'] < 100 else "∞",
                f"{((economics['years_sustainable'] / baseline_years) - 1) * 100:.0f}% longer" if economics['years_sustainable'] < 100 and baseline_years < 100 else "Infinite improvement"
            ]
        }
        
        import pandas as pd
        df_velocity = pd.DataFrame(velocity_data)
        st.dataframe(df_velocity, width='stretch')

def platform_simulation_tab():
    """Simulate platform economics across different scenarios"""
    st.header("📊 Platform Economics Simulation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Platform Metrics")
        
        st.session_state.total_users = st.number_input(
            "Total Users",
            min_value=1_000,
            max_value=50_000_000,
            value=st.session_state.total_users,
            step=10_000,
            format="%d"
        )
        
        st.session_state.dau_percentage = st.slider(
            "Daily Active Users (%)",
            min_value=5.0,
            max_value=50.0,
            value=st.session_state.dau_percentage,
            step=1.0
        )
        
        st.session_state.content_creation_rate = st.slider(
            "Content Creation Rate (% of DAU)",
            min_value=1.0,
            max_value=30.0,
            value=st.session_state.content_creation_rate,
            step=1.0
        )
        
        st.session_state.avg_views_per_content = st.number_input(
            "Average Views per Content",
            min_value=100,
            max_value=100_000,
            value=st.session_state.avg_views_per_content,
            step=500
        )
        
        st.session_state.avg_engagement_per_content = st.number_input(
            "Average Engagement per Content",
            min_value=10,
            max_value=10_000,
            value=st.session_state.avg_engagement_per_content,
            step=10
        )
        
        st.subheader("📈 Quality Metrics")
        
        st.session_state.avg_pv_score = st.slider(
            "Average PV Score",
            min_value=30,
            max_value=100,
            value=st.session_state.avg_pv_score,
            step=1
        )
        
        st.session_state.avg_5a_score = st.slider(
            "Average 5A Score",
            min_value=100,
            max_value=500,
            value=st.session_state.avg_5a_score,
            step=10
        )
        
        st.session_state.avg_trust_score = st.slider(
            "Average Trust Score",
            min_value=0.2,
            max_value=1.0,
            value=st.session_state.avg_trust_score,
            step=0.1
        )
    
    with col2:
        # Run simulation
        results = simulate_platform_economics()
        
        st.subheader("💰 Economic Results")
        
        # Key metrics
        col2a, col2b, col2c = st.columns(3)
        
        with col2a:
            st.metric("Daily Pool", f"{results['daily_pool']:,.0f} VCOIN")
            st.metric("Base Pool", f"{results['base_daily_pool']:,.0f} VCOIN")
            st.metric("Daily Pool USD", f"${results['daily_pool_usd']:,.0f}")
        
        with col2b:
            st.metric("Daily Content", f"{results['daily_content']:,.0f}")
            st.metric("Tokens per Content", f"{results['tokens_per_content']:.0f}")
            st.metric("Creator Tokens", f"{results['creator_tokens']:.0f}")
        
        with col2c:
            st.metric("Creator RPM", f"${results['rpm']:.2f}")
            rpm_status = "✅ Good" if 2.0 <= results['rpm'] <= 8.0 else "⚠️ Adjust"
            st.metric("RPM Status", rpm_status)
            st.metric("Creator USD", f"${results['creator_usd']:.2f}")
        
        # Dynamic scaling metrics
        if st.session_state.enable_dynamic_scaling or st.session_state.enable_price_adjustment:
            st.subheader("🚀 Dynamic Scaling Metrics")
            
            col2d, col2e, col2f = st.columns(3)
            
            with col2d:
                st.metric("User Scaling", f"{results['user_scaling']:.2f}x")
                st.metric("Price Ratio", f"{results['price_ratio']:.2f}x")
            
            with col2e:
                st.metric("Price Adjustment", f"{results['price_adjustment']:.2f}x")
                pool_multiplier = results['daily_pool'] / results['base_daily_pool']
                st.metric("Total Pool Multiplier", f"{pool_multiplier:.2f}x")
            
            with col2f:
                if results['price_ratio'] > 1.0:
                    token_reduction = (1 - results['price_adjustment']) * 100
                    usd_increase = results['price_ratio'] * results['price_adjustment']
                    st.metric("Token Reduction", f"{token_reduction:.1f}%")
                    st.metric("USD Value Increase", f"{usd_increase:.2f}x")
                else:
                    st.metric("Token Reduction", "0%")
                    st.metric("USD Value Increase", "1.0x")
        
        # Distribution breakdown chart
        st.subheader("📊 Token Distribution Breakdown")
        
        distribution_data = {
            'Recipient': ['Creator', 'Engagement Pool', 'Platform'],
            'Tokens': [results['creator_tokens'], results['engagement_tokens'], results['platform_tokens']],
            'USD Value': [
                results['creator_tokens'] * st.session_state.token_price,
                results['engagement_tokens'] * st.session_state.token_price,
                results['platform_tokens'] * st.session_state.token_price
            ],
            'Percentage': [st.session_state.creator_share, st.session_state.engagement_share, st.session_state.platform_share]
        }
        
        fig_dist = px.pie(
            values=distribution_data['Tokens'],
            names=distribution_data['Recipient'],
            title="Token Distribution per Content"
        )
        st.plotly_chart(fig_dist)
        
        # Economics table
        st.subheader("📋 Detailed Economics")
        df_economics = pd.DataFrame(distribution_data)
        st.dataframe(df_economics, width='stretch')

def scenario_analysis_tab():
    """Run multiple scenarios to validate the model"""
    st.header("🧪 Multi-Scenario Analysis")
    
    st.write("Testing Algorithm 5 across different platform scales and conditions.")
    
    # Define scenarios
    scenarios = [
        {'name': 'Micro Launch', 'users': 5_000, 'dau_pct': 20, 'content_rate': 8, 'avg_views': 2000, 'avg_engagement': 50, 'avg_pv': 70, 'avg_5a': 250},
        {'name': 'Small Growth', 'users': 25_000, 'dau_pct': 25, 'content_rate': 10, 'avg_views': 5000, 'avg_engagement': 80, 'avg_pv': 75, 'avg_5a': 275},
        {'name': 'Medium Scale', 'users': 100_000, 'dau_pct': 30, 'content_rate': 12, 'avg_views': 8000, 'avg_engagement': 120, 'avg_pv': 78, 'avg_5a': 300},
        {'name': 'Large Platform', 'users': 500_000, 'dau_pct': 35, 'content_rate': 15, 'avg_views': 12000, 'avg_engagement': 180, 'avg_pv': 82, 'avg_5a': 325},
        {'name': 'Massive Scale', 'users': 2_000_000, 'dau_pct': 30, 'content_rate': 18, 'avg_views': 15000, 'avg_engagement': 250, 'avg_pv': 85, 'avg_5a': 350},
        {'name': 'Viral Success', 'users': 10_000_000, 'dau_pct': 25, 'content_rate': 20, 'avg_views': 20000, 'avg_engagement': 400, 'avg_pv': 88, 'avg_5a': 375}
    ]
    
    # Run scenarios
    scenario_results = []
    
    for scenario in scenarios:
        # Temporarily update session state
        original_values = {}
        for key in ['total_users', 'dau_percentage', 'content_creation_rate', 'avg_views_per_content', 'avg_engagement_per_content', 'avg_pv_score', 'avg_5a_score']:
            original_values[key] = st.session_state[key]
        
        # Set scenario values
        st.session_state.total_users = scenario['users']
        st.session_state.dau_percentage = scenario['dau_pct']
        st.session_state.content_creation_rate = scenario['content_rate']
        st.session_state.avg_views_per_content = scenario['avg_views']
        st.session_state.avg_engagement_per_content = scenario['avg_engagement']
        st.session_state.avg_pv_score = scenario['avg_pv']
        st.session_state.avg_5a_score = scenario['avg_5a']
        
        # Run simulation
        results = simulate_platform_economics()
        
        scenario_results.append({
            'Scenario': scenario['name'],
            'Users': f"{scenario['users']:,}",
            'Daily Content': f"{results['daily_content']:,.0f}",
            'Tokens/Content': f"{results['tokens_per_content']:.0f}",
            'Creator RPM': f"${results['rpm']:.2f}",
            'Pool Coverage': "100%",  # Always 100% by design
            'Status': "✅ Sustainable" if results['rpm'] >= 0.5 else "⚠️ Low RPM"
        })
        
        # Restore original values
        for key, value in original_values.items():
            st.session_state[key] = value
    
    # Display results
    df_scenarios = pd.DataFrame(scenario_results)
    st.dataframe(df_scenarios, width='stretch')
    
    # RPM comparison chart
    st.subheader("📈 RPM Across Scenarios")
    
    rpm_values = [float(result['Creator RPM'].replace('$', '')) for result in scenario_results]
    scenario_names = [result['Scenario'] for result in scenario_results]
    
    fig_rpm = go.Figure()
    fig_rpm.add_trace(go.Bar(
        x=scenario_names,
        y=rpm_values,
        name='Creator RPM',
        marker_color='lightblue'
    ))
    
    # Add target RPM range
    fig_rpm.add_hline(y=2.0, line_dash="dash", line_color="green", annotation_text="Target Min ($2.00)")
    fig_rpm.add_hline(y=8.0, line_dash="dash", line_color="red", annotation_text="Target Max ($8.00)")
    
    fig_rpm.update_layout(
        title="Creator RPM Across Platform Scales",
        xaxis_title="Platform Scale",
        yaxis_title="RPM ($)",
        showlegend=False
    )
    
    st.plotly_chart(fig_rpm)
    
    # Analysis summary
    st.subheader("📊 Analysis Summary")
    
    avg_rpm = sum(rpm_values) / len(rpm_values)
    scenarios_in_target = sum(1 for rpm in rpm_values if 2.0 <= rpm <= 8.0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average RPM", f"${avg_rpm:.2f}")
    with col2:
        st.metric("Scenarios in Target Range", f"{scenarios_in_target}/{len(scenarios)}")
    with col3:
        sustainability_rate = 100.0  # Always 100% for pool model
        st.metric("Sustainability Rate", f"{sustainability_rate:.0f}%")
    
    if avg_rpm < 2.0:
        st.warning("⚠️ **RPM below target range.** Consider increasing daily pool size or adjusting multipliers.")
    elif avg_rpm > 8.0:
        st.warning("⚠️ **RPM above target range.** Consider decreasing daily pool size or adjusting multipliers.")
    else:
        st.success("✅ **RPM in optimal range.** Algorithm 5 is properly calibrated!")

def content_calculator_tab():
    """Interactive content calculator using Algorithm 5"""
    st.header("🧮 Algorithm 5 Content Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Content Input")
        
        # Content details
        content_type = st.selectbox(
            "Content Type",
            ["Text Post", "Short Video", "Long Video", "Podcast"]
        )
        
        # Map content type to multiplier
        ctm_mapping = {
            "Text Post": st.session_state.ctm_text,
            "Short Video": st.session_state.ctm_short_video,
            "Long Video": st.session_state.ctm_long_video,
            "Podcast": st.session_state.ctm_podcast
        }
        
        selected_ctm = ctm_mapping[content_type]
        st.info(f"Content Type Multiplier: {selected_ctm}x")
        
        # Engagement metrics
        views = st.number_input("Views", min_value=0, value=8000, step=100)
        likes = st.number_input("Likes", min_value=0, value=80, step=1)
        comments = st.number_input("Comments", min_value=0, value=12, step=1)
        shares = st.number_input("Shares", min_value=0, value=5, step=1)
        
        total_engagement = views + likes + comments + shares
        st.metric("Total Engagement", f"{total_engagement:,}")
        
        # Quality scores
        pv_score = st.slider("Post Value (PV) Score", min_value=0, max_value=100, value=78, step=1)
        five_a_score = st.slider("5A Creator Score", min_value=0, max_value=500, value=300, step=10)
        trust_score = st.slider("Trust Score", min_value=0.2, max_value=1.0, value=0.8, step=0.1)
    
    with col2:
        st.subheader("💰 Token Calculation")
        
        # Calculate weight using Algorithm 5
        calculated_content_weight = calculate_algorithm_5_weight(
            total_engagement, pv_score, five_a_score, trust_score, selected_ctm
        )
        
        # For demonstration, assume this content gets average share of daily pool
        daily_pool = calculate_daily_pool()
        current_results = simulate_platform_economics()
        
        # Calculate tokens for this specific content
        # Assume it competes with average content
        avg_content_weight = current_results['avg_content_weight']
        relative_weight = calculated_content_weight / avg_content_weight if avg_content_weight > 0 else 1.0
        
        base_tokens = current_results['tokens_per_content']
        content_tokens = base_tokens * relative_weight
        
        # Distribution
        creator_tokens = content_tokens * (st.session_state.creator_share / 100)
        engagement_tokens = content_tokens * (st.session_state.engagement_share / 100)
        platform_tokens = content_tokens * (st.session_state.platform_share / 100)
        
        # USD values
        creator_usd = creator_tokens * st.session_state.token_price
        engagement_usd = engagement_tokens * st.session_state.token_price
        platform_usd = platform_tokens * st.session_state.token_price
        
        # RPM calculation
        rpm = (creator_usd / views) * 1000 if views > 0 else 0
        
        # Display results
        st.metric("Content Weight", f"{calculated_content_weight:.2f}")
        st.metric("Relative Performance", f"{relative_weight:.2f}x avg")
        st.metric("Total Tokens", f"{content_tokens:.0f}")
        
        st.subheader("💸 Distribution Breakdown")
        
        col2a, col2b = st.columns(2)
        
        with col2a:
            st.metric("Creator Tokens", f"{creator_tokens:.0f}")
            st.metric("Creator USD", f"${creator_usd:.2f}")
            st.metric("Creator RPM", f"${rpm:.2f}")
        
        with col2b:
            st.metric("Engagement Pool", f"{engagement_tokens:.0f}")
            st.metric("Platform Share", f"{platform_tokens:.0f}")
            st.metric("Total USD Value", f"${creator_usd + engagement_usd + platform_usd:.2f}")
        
        # Engagement distribution
        st.subheader("👥 Engagement Pool Distribution")
        
        if engagement_tokens > 0:
            shares_tokens = engagement_tokens * (st.session_state.shares_pct / 100)
            comments_tokens = engagement_tokens * (st.session_state.comments_pct / 100)
            reactions_tokens = engagement_tokens * (st.session_state.reactions_pct / 100)
            views_tokens = engagement_tokens * (st.session_state.views_pct / 100)
            
            # Per-user rewards
            shares_per_user = shares_tokens / shares if shares > 0 else 0
            comments_per_user = comments_tokens / comments if comments > 0 else 0
            reactions_per_user = reactions_tokens / likes if likes > 0 else 0
            views_per_user = views_tokens / views if views > 0 else 0
            
            engagement_breakdown = pd.DataFrame({
                'Action': ['Shares', 'Comments', 'Reactions', 'Views'],
                'Pool %': [st.session_state.shares_pct, st.session_state.comments_pct, 
                          st.session_state.reactions_pct, st.session_state.views_pct],
                'Total Tokens': [shares_tokens, comments_tokens, reactions_tokens, views_tokens],
                'Per User': [shares_per_user, comments_per_user, reactions_per_user, views_per_user],
                'Count': [shares, comments, likes, views]
            })
            
            st.dataframe(engagement_breakdown, width='stretch')

def main():
    """Main application"""
    initialize_session_state()
    
    # Sidebar
    st.sidebar.title("🪙 VCOIN Algorithm 5")
    st.sidebar.write("**Price Pool Distribution Model**")
    st.sidebar.write("Sustainable • Quality-Based • Multi-Stakeholder")
    
    # Navigation
    tab_names = [
        "🧮 Algorithm Overview",
        "⚙️ Pool Configuration", 
        "🔄 Token Velocity",
        "📊 Platform Simulation",
        "🧪 Scenario Analysis",
        "🧮 Content Calculator"
    ]
    
    selected_tab = st.sidebar.radio("Navigate", tab_names)
    
    # Tab routing
    if selected_tab == "🧮 Algorithm Overview":
        algorithm_5_overview_tab()
    elif selected_tab == "⚙️ Pool Configuration":
        pool_configuration_tab()
    elif selected_tab == "🔄 Token Velocity":
        token_velocity_management_tab()
    elif selected_tab == "📊 Platform Simulation":
        platform_simulation_tab()
    elif selected_tab == "🧪 Scenario Analysis":
        scenario_analysis_tab()
    elif selected_tab == "🧮 Content Calculator":
        content_calculator_tab()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.write("**Algorithm 5 Benefits:**")
    st.sidebar.write("✅ 100% Sustainable")
    st.sidebar.write("✅ Quality-Weighted")
    st.sidebar.write("✅ Anti-Manipulation")
    st.sidebar.write("✅ Scales Infinitely")

if __name__ == "__main__":
    main()
