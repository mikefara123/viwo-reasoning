#!/usr/bin/env python3
"""
VCOIN Interactive Economic Playground
Streamlit-based interface for testing tokenomics parameters
"""

import math
import random
import json
from datetime import datetime
from typing import Dict, List, Any
from vcoin_economic_engine import VCoinEconomicEngine, VCoinColdStartValuation, ContentMetrics

try:
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install -r requirements.txt")
    exit(1)

# Page configuration
st.set_page_config(
    page_title="VCOIN Economic Playground",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main playground interface with sidebar navigation"""
    
    # Header
    st.markdown('<h1 class="main-header">🪙 VCOIN Economic Playground v2.1</h1>', unsafe_allow_html=True)
    st.markdown("**Test tokenomics parameters and see real-time economic impact**")
    
    # Sidebar navigation
    st.sidebar.title("🧭 VCOIN Analysis Suite")
    st.sidebar.markdown("---")
    
    # Group simulations by category
    st.sidebar.markdown("### 📊 Core Economics")
    core_options = [
        "🎛️ Parameter Testing",
        "💰 Price Discovery", 
        "🎬 Content Calculator",
        "📈 Economy Scale Simulator",
        "⚔️ A/B Comparison"
    ]
    
    st.sidebar.markdown("### 💼 Investment Planning")
    investment_options = [
        "🏦 Token Initial Valuation",
        "🔄 Reverse Simulation",
        "🚀 Cold Start Scenario"
    ]
    
    st.sidebar.markdown("### 🔬 Advanced Analysis")
    advanced_options = [
        "🏛️ Governance & DAO",
        "📅 Vesting & Unlocks",
        "🛡️ Security & Stress Test"
    ]
    
    # Create grouped selection
    all_options = core_options + investment_options + advanced_options
    
    selected_tab = st.sidebar.radio(
        "Select Analysis Tool:",
        all_options,
        index=0
    )
    
    # Add helpful info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Quick Tips:")
    
    if selected_tab in core_options:
        st.sidebar.info("🎯 **Core Economics**: Test fundamental tokenomics parameters and economic sustainability.")
    elif selected_tab in investment_options:
        st.sidebar.info("💼 **Investment Planning**: Calculate ICO pricing, plan token launch, and set target earnings.")
    elif selected_tab in advanced_options:
        st.sidebar.info("🔬 **Advanced Analysis**: Test governance, vesting schedules, and economic resilience.")
    
    # Add current selection indicator
    st.sidebar.markdown("---")
    st.sidebar.success(f"📍 **Current:** {selected_tab.split(' ', 1)[1]}")
    
    # Add app info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About VCOIN")
    st.sidebar.markdown("""
    **Professional tokenomics simulation suite for ViWo's social media platform.**
    
    🎯 **Features:**
    - 10 comprehensive analysis tools
    - Professional export reports
    - Ultra-precise token pricing
    - Economic resilience testing
    
    🚀 **Perfect for:**
    - Investor presentations
    - Team planning sessions
    - ICO preparation
    - Economic optimization
    """)
    
    # Display selected interface
    if selected_tab == "🎛️ Parameter Testing":
        parameter_testing_interface()
    elif selected_tab == "💰 Price Discovery":
        price_discovery_interface()
    elif selected_tab == "🎬 Content Calculator":
        content_calculator_interface()
    elif selected_tab == "📈 Economy Scale Simulator":
        economy_scale_simulator_interface()
    elif selected_tab == "⚔️ A/B Comparison":
        ab_comparison_interface()
    elif selected_tab == "🏦 Token Initial Valuation":
        token_initial_valuation_interface()
    elif selected_tab == "🔄 Reverse Simulation":
        reverse_simulation_interface()
    elif selected_tab == "🚀 Cold Start Scenario":
        cold_start_scenario_interface()
    elif selected_tab == "🏛️ Governance & DAO":
        governance_dao_interface()
    elif selected_tab == "📅 Vesting & Unlocks":
        vesting_unlocks_interface()
    elif selected_tab == "🛡️ Security & Stress Test":
        security_stress_test_interface()

def token_initial_valuation_interface():
    """Token Initial Valuation for ICO/ICP"""
    st.header("🏦 Token Initial Valuation Calculator")
    st.markdown("**Calculate initial token price for investors and ICP sale based on R&D investment, liquidity backing, and market projections**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💰 Investment Parameters")
        
        # Core investment parameters
        rd_investment = st.number_input("R&D Investment ($)", value=500000, min_value=0, step=10000,
                                       help="Total spent on research, development, and tokenomics design")
        
        liquidity_backing = st.number_input("Initial Liquidity Backing ($)", value=100000, min_value=0, step=5000,
                                          help="Cash allocated to support initial market liquidity")
        
        operational_costs = st.number_input("Annual Operational Costs ($)", value=200000, min_value=0, step=10000,
                                          help="Yearly costs for development, marketing, and operations")
        
        st.subheader("🪙 Token Supply Parameters")
        
        total_token_supply = st.number_input("Total Token Supply", value=10000000000, min_value=1000000, step=1000000,
                                           help="Maximum tokens that will ever exist (10B VCOIN)")
        
        ico_token_amount = st.number_input("Tokens for ICO Sale", value=100000000, min_value=1000000, step=1000000,
                                         help="Number of tokens to sell in initial offering")
        
        circulating_at_launch = st.number_input("Circulating Supply at Launch", value=1000000000, min_value=ico_token_amount, step=1000000,
                                               help="Total tokens available at launch (including ICO)")
        
        st.subheader("📈 Market Projections")
        
        year1_revenue = st.number_input("Year 1 Projected Revenue ($)", value=500000, min_value=0, step=25000,
                                       help="Expected platform revenue in first year")
        
        revenue_growth_rate = st.slider("Annual Revenue Growth Rate (%)", min_value=0, max_value=200, value=50, step=5,
                                       help="Expected yearly revenue growth percentage")
        
        user_growth_year1 = st.number_input("Year 1 Expected Users", value=100000, min_value=1000, step=10000,
                                          help="Expected user base by end of year 1")
        
        user_growth_rate = st.slider("Annual User Growth Rate (%)", min_value=0, max_value=300, value=100, step=10,
                                    help="Expected yearly user growth percentage")
    
    with col2:
        st.subheader("⚙️ Valuation Settings")
        
        discount_rate = st.slider("Discount Rate (%)", min_value=10, max_value=80, value=40, step=5,
                                help="Risk-adjusted discount rate for DCF analysis (crypto typical: 30-60%)")
        
        terminal_growth_rate = st.slider("Terminal Growth Rate (%)", min_value=0, max_value=10, value=3, step=1,
                                       help="Long-term sustainable growth rate")
        
        forecast_years = st.selectbox("DCF Forecast Period (years)", [3, 5, 7, 10], index=1,
                                    help="Number of years to project cash flows")
        
        token_velocity = st.slider("Expected Token Velocity", min_value=1.0, max_value=20.0, value=8.0, step=0.5,
                                 help="How many times tokens change hands per year (higher = lower price)")
        
        platform_take_rate = st.slider("Platform Take Rate (%)", min_value=5, max_value=25, value=10, step=1,
                                      help="Percentage of transaction volume retained as revenue")
        
        st.subheader("🎯 Market Context")
        
        comparable_market_cap = st.number_input("Comparable Project Market Cap ($M)", value=50, min_value=1, step=5,
                                              help="Market cap of similar projects for benchmarking")
        
        market_cap_multiple = st.slider("Market Cap Multiple", min_value=0.1, max_value=3.0, value=0.5, step=0.1,
                                       help="Multiple of comparable market cap to target")
        
        icp_price = st.number_input("Current ICP Price ($)", value=4.82, min_value=0.1, step=0.1,
                                  help="Current Internet Computer Protocol token price")
    
    # Execute button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        execute_valuation = st.button("🚀 Execute Valuation", type="primary", width="stretch", key="valuation_execute")
    
    with col2:
        export_results = st.button("📄 Export Results", width="stretch", key="valuation_export")
    
    with col3:
        reset_defaults = st.button("🔄 Reset to Defaults", width="stretch", key="valuation_reset")
    
    # Reset functionality
    if reset_defaults:
        st.rerun()
    
    # Only calculate and show results when Execute is clicked
    if execute_valuation or 'valuation_executed' not in st.session_state:
        st.session_state.valuation_executed = True
        
        # Calculate valuations
        st.markdown("---")
        st.header("💎 Valuation Results")
        
        # Method 1: Asset-Based Valuation (R&D + Liquidity)
        asset_value = rd_investment + liquidity_backing
        asset_based_price = asset_value / ico_token_amount
    
        # Method 2: DCF Analysis
        dcf_value = calculate_dcf_valuation(year1_revenue, revenue_growth_rate, discount_rate, 
                                           terminal_growth_rate, forecast_years, platform_take_rate)
        dcf_token_price = dcf_value / circulating_at_launch
        
        # Method 3: Market Cap Multiple
        target_market_cap = comparable_market_cap * 1000000 * market_cap_multiple
        market_cap_price = target_market_cap / circulating_at_launch
        
        # Method 4: Equation of Exchange (MV = PQ)
        transaction_volume = calculate_transaction_volume(user_growth_year1, user_growth_rate, year1_revenue, revenue_growth_rate)
        exchange_price = transaction_volume / (circulating_at_launch * token_velocity)
        
        # Method 5: Revenue Multiple
        revenue_multiple = 10  # Typical SaaS multiple
        revenue_based_value = year1_revenue * revenue_multiple
        revenue_based_price = revenue_based_value / circulating_at_launch
    
        # Display results
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.metric("💰 Asset-Based Price", f"${asset_based_price:.4f}", 
                     help="Based on R&D investment + liquidity backing")
            st.metric("📊 DCF Price", f"${dcf_token_price:.4f}",
                     help="Discounted Cash Flow valuation")
        
        with col2:
            st.metric("🏢 Market Cap Multiple", f"${market_cap_price:.4f}",
                     help="Based on comparable project multiples")
            st.metric("🔄 Exchange Equation", f"${exchange_price:.4f}",
                     help="MV = PQ equation of exchange model")
        
        with col3:
            st.metric("📈 Revenue Multiple", f"${revenue_based_price:.4f}",
                     help="Based on revenue multiples")
            
            # Weighted average recommendation
            prices = [asset_based_price, dcf_token_price, market_cap_price, exchange_price, revenue_based_price]
            weights = [0.25, 0.30, 0.20, 0.15, 0.10]  # DCF weighted highest
            weighted_price = sum(p * w for p, w in zip(prices, weights))
            
            st.metric("🎯 Recommended Price", f"${weighted_price:.4f}",
                     help="Weighted average of all methods")
    
        # ICO calculations
        st.subheader("🚀 ICO Analysis")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            ico_raise_usd = ico_token_amount * weighted_price
            st.metric("💵 Total ICO Raise (USD)", f"${ico_raise_usd:,.0f}")
            
            ico_raise_icp = ico_raise_usd / icp_price
            st.metric("🪙 Total ICO Raise (ICP)", f"{ico_raise_icp:,.0f} ICP")
        
        with col2:
            market_cap_at_launch = circulating_at_launch * weighted_price
            st.metric("📊 Market Cap at Launch", f"${market_cap_at_launch:,.0f}")
            
            fdv = total_token_supply * weighted_price
            st.metric("💎 Fully Diluted Value", f"${fdv:,.0f}")
        
        with col3:
            ico_percentage = (ico_token_amount / total_token_supply) * 100
            st.metric("📊 ICO % of Total Supply", f"{ico_percentage:.1f}%")
            
            circulating_percentage = (circulating_at_launch / total_token_supply) * 100
            st.metric("🔄 Circulating % at Launch", f"{circulating_percentage:.1f}%")
        
        # Store results in session state for export
        st.session_state.valuation_results = {
            'input_parameters': {
                'rd_investment': rd_investment,
                'liquidity_backing': liquidity_backing,
                'operational_costs': operational_costs,
                'total_token_supply': total_token_supply,
                'ico_token_amount': ico_token_amount,
                'circulating_at_launch': circulating_at_launch,
                'year1_revenue': year1_revenue,
                'revenue_growth_rate': revenue_growth_rate,
                'user_growth_year1': user_growth_year1,
                'user_growth_rate': user_growth_rate,
                'discount_rate': discount_rate,
                'terminal_growth_rate': terminal_growth_rate,
                'forecast_years': forecast_years,
                'token_velocity': token_velocity,
                'platform_take_rate': platform_take_rate,
                'comparable_market_cap': comparable_market_cap,
                'market_cap_multiple': market_cap_multiple,
                'icp_price': icp_price
            },
            'valuation_results': {
                'asset_based_price': asset_based_price,
                'dcf_token_price': dcf_token_price,
                'market_cap_price': market_cap_price,
                'exchange_price': exchange_price,
                'revenue_based_price': revenue_based_price,
                'weighted_price': weighted_price,
                'ico_raise_usd': ico_raise_usd,
                'ico_raise_icp': ico_raise_icp,
                'market_cap_at_launch': market_cap_at_launch,
                'fdv': fdv,
                'ico_percentage': ico_percentage,
                'circulating_percentage': circulating_percentage
            }
        }
    
        # Formula explanations
        st.markdown("---")
        st.subheader("📝 Valuation Formulas & Methodology")
        
        with st.expander("🔢 See Detailed Formulas"):
            st.markdown("""
        ### 1. Asset-Based Valuation
        ```
        Asset Value = R&D Investment + Liquidity Backing
        Token Price = Asset Value ÷ ICO Token Amount
        
        Current: ${:,.0f} ÷ {:,.0f} = ${:.4f}
        ```
        
        ### 2. Discounted Cash Flow (DCF)
        ```
        DCF = Σ(CFt ÷ (1 + r)^t) + Terminal Value
        Where:
        - CFt = Cash Flow in year t
        - r = Discount Rate ({:.1f}%)
        - Terminal Value = CF_final × (1 + g) ÷ (r - g)
        - g = Terminal Growth Rate ({:.1f}%)
        
        Present Value: ${:,.0f}
        Token Price: ${:,.0f} ÷ {:,.0f} = ${:.4f}
        ```
        
        ### 3. Market Cap Multiple
        ```
        Target Market Cap = Comparable Market Cap × Multiple
        Token Price = Target Market Cap ÷ Circulating Supply
        
        Current: ${:.1f}M × {:.1f} ÷ {:,.0f} = ${:.4f}
        ```
        
        ### 4. Equation of Exchange (MV = PQ)
        ```
        M × V = P × Q
        Token Price = (P × Q) ÷ (M × V)
        Where:
        - M = Money Supply (Circulating Tokens)
        - V = Velocity ({:.1f})
        - P × Q = Transaction Volume
        
        Current: ${:,.0f} ÷ ({:,.0f} × {:.1f}) = ${:.4f}
        ```
        
        ### 5. Revenue Multiple
        ```
        Valuation = Annual Revenue × Multiple
        Token Price = Valuation ÷ Circulating Supply
        
        Current: ${:,.0f} × {:.0f} ÷ {:,.0f} = ${:.4f}
        ```
        
        ### 6. Weighted Average
        ```
        Final Price = Σ(Method Price × Weight)
        Weights: Asset(25%) + DCF(30%) + Market(20%) + Exchange(15%) + Revenue(10%)
        
        Result: ${:.4f}
        ```
        """.format(
            asset_value, ico_token_amount, asset_based_price,
            discount_rate, terminal_growth_rate, dcf_value, dcf_value, circulating_at_launch, dcf_token_price,
            comparable_market_cap, market_cap_multiple, circulating_at_launch, market_cap_price,
            token_velocity, transaction_volume, circulating_at_launch, token_velocity, exchange_price,
            year1_revenue, revenue_multiple, circulating_at_launch, revenue_based_price,
            weighted_price
        ))
    
        # Risk analysis
        st.markdown("---")
        st.subheader("⚠️ Risk Analysis & Sensitivity")
        
        # Sensitivity analysis
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🔺 Upside Scenarios (+50% price):**")
            st.write(f"• Revenue grows {revenue_growth_rate + 25}% annually")
            st.write(f"• User adoption exceeds {user_growth_year1:,.0f} by 50%")
            st.write(f"• Market cap multiple reaches {market_cap_multiple * 1.5:.1f}x")
            st.write(f"• **Upside Price: ${weighted_price * 1.5:.4f}**")
        
        with col2:
            st.markdown("**🔻 Downside Scenarios (-30% price):**")
            st.write(f"• Revenue grows only {max(0, revenue_growth_rate - 25)}% annually")
            st.write(f"• User adoption reaches only {user_growth_year1 * 0.7:,.0f}")
            st.write(f"• Higher token velocity ({token_velocity * 1.5:.1f}x)")
            st.write(f"• **Downside Price: ${weighted_price * 0.7:.4f}**")
    
    # Export functionality
    if export_results and 'valuation_results' in st.session_state:
        results = st.session_state.valuation_results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        export_content = f"""VCOIN TOKEN INITIAL VALUATION REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== INPUT PARAMETERS ===
R&D Investment: ${results['input_parameters']['rd_investment']:,.0f}
Initial Liquidity Backing: ${results['input_parameters']['liquidity_backing']:,.0f}
Annual Operational Costs: ${results['input_parameters']['operational_costs']:,.0f}
Total Token Supply: {results['input_parameters']['total_token_supply']:,.0f} VCOIN
ICO Token Amount: {results['input_parameters']['ico_token_amount']:,.0f} VCOIN
Circulating Supply at Launch: {results['input_parameters']['circulating_at_launch']:,.0f} VCOIN
Year 1 Projected Revenue: ${results['input_parameters']['year1_revenue']:,.0f}
Annual Revenue Growth Rate: {results['input_parameters']['revenue_growth_rate']:.1f}%
Year 1 Expected Users: {results['input_parameters']['user_growth_year1']:,.0f}
Annual User Growth Rate: {results['input_parameters']['user_growth_rate']:.1f}%
Discount Rate: {results['input_parameters']['discount_rate']:.1f}%
Terminal Growth Rate: {results['input_parameters']['terminal_growth_rate']:.1f}%
DCF Forecast Period: {results['input_parameters']['forecast_years']} years
Expected Token Velocity: {results['input_parameters']['token_velocity']:.1f}
Platform Take Rate: {results['input_parameters']['platform_take_rate']:.1f}%
Comparable Market Cap: ${results['input_parameters']['comparable_market_cap']:.1f}M
Market Cap Multiple: {results['input_parameters']['market_cap_multiple']:.1f}x
Current ICP Price: ${results['input_parameters']['icp_price']:.2f}

=== VALUATION RESULTS ===
Asset-Based Price: ${results['valuation_results']['asset_based_price']:.4f}
DCF Price: ${results['valuation_results']['dcf_token_price']:.4f}
Market Cap Multiple Price: ${results['valuation_results']['market_cap_price']:.4f}
Exchange Equation Price: ${results['valuation_results']['exchange_price']:.4f}
Revenue Multiple Price: ${results['valuation_results']['revenue_based_price']:.4f}

RECOMMENDED PRICE: ${results['valuation_results']['weighted_price']:.4f}

=== ICO ANALYSIS ===
Total ICO Raise (USD): ${results['valuation_results']['ico_raise_usd']:,.0f}
Total ICO Raise (ICP): {results['valuation_results']['ico_raise_icp']:,.0f} ICP
Market Cap at Launch: ${results['valuation_results']['market_cap_at_launch']:,.0f}
Fully Diluted Value: ${results['valuation_results']['fdv']:,.0f}
ICO % of Total Supply: {results['valuation_results']['ico_percentage']:.1f}%
Circulating % at Launch: {results['valuation_results']['circulating_percentage']:.1f}%

=== VALUATION METHODOLOGY ===
1. Asset-Based: (R&D + Liquidity) ÷ ICO Tokens
2. DCF: Discounted Cash Flow with {results['input_parameters']['discount_rate']:.1f}% discount rate
3. Market Cap Multiple: Comparable projects × {results['input_parameters']['market_cap_multiple']:.1f}x multiple
4. Exchange Equation: MV = PQ model with {results['input_parameters']['token_velocity']:.1f} velocity
5. Revenue Multiple: Annual revenue × 10x SaaS multiple

Weighted Average: Asset(25%) + DCF(30%) + Market(20%) + Exchange(15%) + Revenue(10%)

=== RISK SCENARIOS ===
Upside Price (+50%): ${results['valuation_results']['weighted_price'] * 1.5:.4f}
Downside Price (-30%): ${results['valuation_results']['weighted_price'] * 0.7:.4f}
"""
        
        st.download_button(
            label="📄 Download Valuation Report",
            data=export_content,
            file_name=f"vcoin_valuation_report_{timestamp}.txt",
            mime="text/plain",
            width="stretch"
        )

def calculate_dcf_valuation(year1_revenue, growth_rate, discount_rate, terminal_growth, years, take_rate):
    """Calculate DCF valuation"""
    dcf_value = 0
    growth_decimal = growth_rate / 100
    discount_decimal = discount_rate / 100
    terminal_decimal = terminal_growth / 100
    
    # Calculate yearly cash flows
    for year in range(1, years + 1):
        revenue = year1_revenue * ((1 + growth_decimal) ** year)
        cash_flow = revenue * (take_rate / 100)  # Platform's share
        present_value = cash_flow / ((1 + discount_decimal) ** year)
        dcf_value += present_value
    
    # Terminal value
    final_year_revenue = year1_revenue * ((1 + growth_decimal) ** years)
    final_cash_flow = final_year_revenue * (take_rate / 100)
    terminal_cash_flow = final_cash_flow * (1 + terminal_decimal)
    terminal_value = terminal_cash_flow / (discount_decimal - terminal_decimal)
    terminal_pv = terminal_value / ((1 + discount_decimal) ** years)
    
    return dcf_value + terminal_pv

def calculate_transaction_volume(users_year1, user_growth, revenue_year1, revenue_growth):
    """Calculate expected transaction volume for equation of exchange"""
    # Estimate transaction volume based on users and revenue
    avg_revenue_per_user = revenue_year1 / users_year1
    transaction_multiplier = 20  # Assume transactions are 20x revenue (typical for platforms)
    
    return revenue_year1 * transaction_multiplier

def run_enhanced_parameter_simulation(params: Dict[str, Any], days: int, scenario: str) -> List[Dict[str, Any]]:
    """Run enhanced economic simulation with comprehensive parameters"""
    
    # Initialize simulation results
    results = []
    
    # Define scenario parameters
    scenario_configs = {
        "Conservative": {
            'user_growth_rate': 0.02,  # 2% monthly
            'revenue_growth_rate': 0.015,  # 1.5% monthly
            'churn_multiplier': 1.0
        },
        "Moderate": {
            'user_growth_rate': 0.05,  # 5% monthly
            'revenue_growth_rate': 0.03,  # 3% monthly
            'churn_multiplier': 0.8
        },
        "Aggressive": {
            'user_growth_rate': 0.10,  # 10% monthly
            'revenue_growth_rate': 0.06,  # 6% monthly
            'churn_multiplier': 0.6
        }
    }
    
    config = scenario_configs[scenario]
    
    # Initial values
    current_supply = params['initial_supply']
    current_users = params['daily_users']
    current_revenue = params['daily_revenue']
    current_price = params['initial_price']  # Use user-specified starting price
    staked_tokens = current_supply * 0.3  # Assume 30% initially staked
    
    # Calculate initial market cap based on starting price
    initial_market_cap = current_supply * current_price
    
    # Initialize monthly metrics outside the loop
    monthly_metrics = {
        'new_users_added': 0,
        'users_churned': 0,
        'net_user_change': 0,
        'churn_rate': 0
    }
    
    # Simulate each day
    for day in range(days):
        # Monthly growth (every 30 days)
        if day % 30 == 0 and day > 0:
            # Use user-specified acquisition rate instead of scenario-based growth
            new_users_added = current_users * params['monthly_acquisition_rate']
            users_churned = current_users * params['monthly_churn_rate'] * config['churn_multiplier']
            net_user_change = new_users_added - users_churned
            current_users = max(1, current_users + net_user_change)
            
            # Store monthly metrics
            monthly_metrics = {
                'new_users_added': new_users_added,
                'users_churned': users_churned,
                'net_user_change': net_user_change,
                'churn_rate': params['monthly_churn_rate'] * config['churn_multiplier']
            }
            
            # Revenue growth
            current_revenue = current_revenue * (1 + config['revenue_growth_rate'])
        
        # Daily calculations - align with Content Calculator logic
        daily_creators = current_users * params['content_creation_rate']
        daily_content_pieces = daily_creators * 2  # Assume each creator makes 2 pieces of content per day
        
        # Use Content Calculator logic for reward pool calculation
        if current_revenue > 0:
            # Revenue-backed mode: 90% of revenue to rewards (matching Content Calculator)
            daily_rewards_pool_usd = current_revenue * 0.90
            daily_rewards_pool_tokens = daily_rewards_pool_usd / current_price
        else:
            # Bootstrap mode: use token minting (matching Content Calculator bootstrap)
            daily_token_mint = current_supply * (params['annual_inflation_rate'] / 365)
            daily_rewards_pool_tokens = daily_token_mint
            daily_rewards_pool_usd = daily_rewards_pool_tokens * current_price
        
        # Calculate per-content reward (matching Content Calculator approach)
        base_reward_per_content = daily_rewards_pool_tokens / max(1, daily_content_pieces)
        
        # Apply average multipliers (simplified from Content Calculator's complex engine)
        avg_content_multiplier = 1.2  # Average between different content types
        avg_engagement_multiplier = 1.5  # Average engagement boost
        avg_quality_multiplier = 1.3  # Average 5A and accuracy multiplier
        
        total_multiplier = avg_content_multiplier * avg_engagement_multiplier * avg_quality_multiplier
        enhanced_reward_per_content = base_reward_per_content * total_multiplier
        
        # Total content rewards (all creators combined)
        total_content_rewards = enhanced_reward_per_content * daily_content_pieces
        
        # Distribute according to our tokenomics model
        creator_rewards = total_content_rewards * params['creator_share']
        engagement_rewards = total_content_rewards * params['engagement_share'] 
        commission_rewards = total_content_rewards * params['commission_share']
        royalty_rewards = total_content_rewards * params['royalty_share']
        
        # Transaction fees
        daily_transactions = current_users * (params['avg_session_minutes'] / 30)  # Transactions per session
        transaction_fees = daily_transactions * current_price * params['transaction_fee_percent']
        
        # Staking rewards
        daily_staking_rewards = staked_tokens * (params['staking_apy'] / 365)
        
        # Token burns
        commission_burned = commission_rewards * params['commission_burn_rate']
        total_burned = commission_burned
        
        # Token minting (inflation) - use actual minting from reward calculation
        if current_revenue > 0:
            # In revenue mode, inflation is separate from rewards
            daily_inflation = current_supply * (params['annual_inflation_rate'] / 365)
        else:
            # In bootstrap mode, inflation IS the reward minting (matching Content Calculator)
            daily_inflation = daily_token_mint
        current_supply = min(params['max_supply'], current_supply + daily_inflation - total_burned)
        
        # Price calculation (more realistic based on starting price and growth)
        # Combine revenue growth with initial market cap
        revenue_multiple = 8 + (current_revenue / params['daily_revenue'] - 1) * 2  # Dynamic multiple
        theoretical_market_cap = current_revenue * 365 * revenue_multiple
        
        # Price influenced by both market cap and initial price stability
        market_price = theoretical_market_cap / current_supply
        price_stability_factor = 0.7  # 70% market-driven, 30% price stability
        current_price = (market_price * price_stability_factor) + (current_price * (1 - price_stability_factor))
        
        # Calculate actual market cap based on final token price and supply
        market_cap = current_supply * current_price
        
        # Update staked tokens
        staking_rate = min(0.6, 0.3 + (params['staking_apy'] - 0.05) * 2)  # Higher APY = more staking
        staked_tokens = current_supply * staking_rate
        
        # Calculate comprehensive tokenomics metrics
        circulating_for_content = current_supply - staked_tokens  # Tokens available for content rewards
        circulating_for_trade = circulating_for_content * 0.7  # 70% available for trading
        circulating_for_nft = circulating_for_content * 0.3   # 30% for NFT/content economy
        
        # Calculate cumulative metrics
        if day == 0:
            cumulative_minted = daily_inflation
            cumulative_burned = total_burned
        else:
            prev_result = results[-1] if results else {'cumulative_minted': 0, 'cumulative_burned': 0}
            cumulative_minted = prev_result.get('cumulative_minted', 0) + daily_inflation
            cumulative_burned = prev_result.get('cumulative_burned', 0) + total_burned
        
        # Net user growth (accounting for churn)
        if day % 30 == 0 and day > 0:
            net_monthly_growth = monthly_metrics.get('net_user_change', 0)
            monthly_growth_rate = net_monthly_growth / (current_users - net_monthly_growth) if current_users > net_monthly_growth else 0
        else:
            net_monthly_growth = 0
            monthly_growth_rate = 0
        
        # Calculate metrics
        result = {
            'day': day,
            'current_supply': current_supply,
            'token_price': current_price,
            'market_cap': market_cap,
            'daily_users': current_users,
            'daily_creators': daily_creators,
            'creator_rewards': creator_rewards,
            'engagement_rewards': engagement_rewards,
            'commission_rewards': commission_rewards,
            'royalty_rewards': royalty_rewards,
            'total_rewards': creator_rewards + engagement_rewards + commission_rewards + royalty_rewards,
            'daily_content_pieces': daily_content_pieces,
            'base_reward_per_content': base_reward_per_content,
            'enhanced_reward_per_content': enhanced_reward_per_content,
            'total_multiplier': total_multiplier,
            'total_burned': total_burned,
            'daily_minted': daily_inflation,
            'cumulative_minted': cumulative_minted,
            'cumulative_burned': cumulative_burned,
            'net_token_flow': daily_inflation - total_burned,
            'transaction_fees': transaction_fees,
            'platform_revenue': current_revenue,
            'staked_tokens': staked_tokens,
            'staked_percentage': (staked_tokens / current_supply) * 100,
            'circulating_for_content': circulating_for_content,
            'circulating_for_trade': circulating_for_trade,
            'circulating_for_nft': circulating_for_nft,
            'current_inflation_rate': (daily_inflation / current_supply) * 365 * 100,
            'actual_token_velocity': params['token_velocity'],
            'daily_burn_rate': (total_burned / current_supply) * 100,
            'avg_creator_earnings': (creator_rewards * current_price) / max(1, daily_creators),
            'avg_user_earnings': (engagement_rewards * current_price) / current_users,
            'user_retention_rate': 100 - (params['monthly_churn_rate'] * config['churn_multiplier'] * 100),
            'acquisition_roi': (current_revenue / current_users * 30) / params['user_acquisition_cost'],
            'revenue_cost_ratio': current_revenue / (daily_rewards_pool_usd + params['user_acquisition_cost'] * current_users / 30),
            'health_score': min(100, (current_price / params['initial_price']) * 50 + 
                              (current_users / params['daily_users']) * 25 + 
                              (staking_rate * 25)),
            'platform_health': min(100, (current_revenue / params['daily_revenue']) * 40 + 
                                 (current_users / params['daily_users']) * 35 + 
                                 ((100 - params['monthly_churn_rate'] * 100) / 100) * 25),
            'token_economy_score': min(100, (1 - params['annual_inflation_rate']) * 30 + 
                                     staking_rate * 40 + 
                                     (total_burned / daily_inflation if daily_inflation > 0 else 1) * 30),
            'user_satisfaction': min(100, (params['avg_session_minutes'] / 60) * 30 + 
                                   (current_price / params['initial_price']) * 35 + 
                                   ((engagement_rewards * current_price) / current_users) * 35),
            # New comprehensive metrics
            'starting_token_value': params['initial_price'],
            'ending_token_value': current_price,
            'total_value_change': ((current_price / params['initial_price']) - 1) * 100,
            'net_monthly_growth': net_monthly_growth,
            'monthly_growth_rate': monthly_growth_rate,
            # Monthly metrics (only on month boundaries)
            'new_users_added': monthly_metrics.get('new_users_added', 0),
            'users_churned': monthly_metrics.get('users_churned', 0),
            'monthly_churn_rate': monthly_metrics.get('churn_rate', 0)
        }
        
        results.append(result)
    
    return results

def display_enhanced_simulation_results(results: List[Dict[str, Any]], params: Dict[str, Any], months: int):
    """Display enhanced simulation results with comprehensive metrics"""
    
    if not results:
        st.error("No simulation results to display")
        return
    
    final_result = results[-1]
    initial_result = results[0]
    
    st.header("📊 Enhanced Simulation Results")
    st.markdown(f"**{months}-Month Economic Simulation Complete**")
    
    # Starting price impact summary
    st.subheader("💰 Token Price Impact Analysis")
    starting_price = params['initial_price']
    
    # Calculation verification section
    st.subheader("🔍 Calculation Verification")
    
    with st.expander("📊 Key Metrics Breakdown", expanded=False):
        st.markdown("**Final Calculations Verification:**")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            **Token Price Calculation:**
            - Starting Price: ${starting_price:.7f}
            - Final Price: ${final_result['token_price']:.7f}
            - Price Change: {((final_result['token_price'] / initial_result['token_price']) - 1) * 100:+.1f}%
            
            **Market Cap Calculation:**
            - Token Supply: {final_result['current_supply']:,.0f}
            - Token Price: ${final_result['token_price']:.7f}
            - Market Cap: {final_result['current_supply']:,.0f} × ${final_result['token_price']:.7f} = ${final_result['market_cap']:,.0f}
            """)
        
        with col2:
            st.markdown(f"""
            **User Metrics:**
            - Starting Users: {initial_result['daily_users']:,.0f}
            - Final Users: {final_result['daily_users']:,.0f}
            - User Change: {((final_result['daily_users'] / initial_result['daily_users']) - 1) * 100:+.1f}%
            - Monthly Churn Rate: {params['monthly_churn_rate'] * 100:.1f}%
            - User Retention: {final_result['user_retention_rate']:.1f}%
            
            **Supply Metrics:**
            - Starting Supply: {initial_result['current_supply']:,.0f}
            - Final Supply: {final_result['current_supply']:,.0f}
            - Supply Change: {((final_result['current_supply'] / initial_result['current_supply']) - 1) * 100:+.1f}%
            """)
        
        # Verify market cap calculation
        calculated_market_cap = final_result['current_supply'] * final_result['token_price']
        market_cap_match = abs(calculated_market_cap - final_result['market_cap']) < 1
        
        if market_cap_match:
            st.success("✅ Market Cap calculation verified: Supply × Price = Market Cap")
        else:
            st.error(f"❌ Market Cap mismatch: Expected ${calculated_market_cap:,.0f}, Got ${final_result['market_cap']:,.0f}")
        
        # Verify retention calculation
        expected_retention = 100 - (params['monthly_churn_rate'] * 100)
        retention_match = abs(expected_retention - final_result['user_retention_rate']) < 0.1
        
        if retention_match:
            st.success("✅ User Retention calculation verified")
        else:
            st.warning(f"⚠️ Retention calculation: Expected {expected_retention:.1f}%, Got {final_result['user_retention_rate']:.1f}%")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        daily_token_pool = (params['daily_revenue'] * 0.7) / starting_price
        st.metric("Daily Token Reward Pool", f"{daily_token_pool:,.0f} VCOIN")
        creator_daily_tokens = daily_token_pool * params['creator_share']
        st.metric("Creator Daily Tokens", f"{creator_daily_tokens:,.0f} VCOIN")
    
    with col2:
        engagement_daily_tokens = daily_token_pool * params['engagement_share']
        st.metric("Engagement Daily Tokens", f"{engagement_daily_tokens:,.0f} VCOIN")
        avg_user_tokens = engagement_daily_tokens / params['daily_users']
        st.metric("Avg User Daily Tokens", f"{avg_user_tokens:.1f} VCOIN")
    
    with col3:
        avg_creator_usd = (creator_daily_tokens / (params['daily_users'] * params['content_creation_rate'])) * starting_price
        st.metric("Avg Creator Daily USD", f"${avg_creator_usd:.2f}")
        avg_user_usd = avg_user_tokens * starting_price
        st.metric("Avg User Daily USD", f"${avg_user_usd:.3f}")
    
    # Key Metrics
    st.subheader("📊 Simulation Results Summary")
    # Main KPI display matching your format
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        price_change = ((final_result['token_price'] / initial_result['token_price']) - 1) * 100
        st.metric("Final Token Price", f"${final_result['token_price']:.7f}", f"{price_change:+.1f}%")
    
    with col2:
        st.metric("Market Cap", f"${final_result['market_cap']:,.0f}")
    
    with col3:
        user_change = ((final_result['daily_users'] / initial_result['daily_users']) - 1) * 100
        st.metric("Daily Active Users", f"{final_result['daily_users']:,.0f}", f"{user_change:+.1f}%")
    
    with col4:
        st.metric("User Retention", f"{final_result['user_retention_rate']:.1f}%")
    
    with col5:
        supply_change = ((final_result['current_supply'] / initial_result['current_supply']) - 1) * 100
        st.metric("Token Supply", f"{final_result['current_supply']:,.0f}", f"{supply_change:+.1f}%")
    
    # Comprehensive Tokenomics Analysis
    st.markdown("---")
    st.subheader("🏆 Comprehensive Tokenomics Analysis")
    
    # Token Supply & Flow Analysis
    st.markdown("#### 🪙 Token Supply & Flow Analysis")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.metric("Total Minted Tokens", f"{final_result['cumulative_minted']:,.0f} VCOIN", 
                 f"During {months}-month period")
    
    with col2:
        st.metric("Total Burned Tokens", f"{final_result['cumulative_burned']:,.0f} VCOIN", 
                 f"Deflationary pressure")
    
    with col3:
        net_flow = final_result['cumulative_minted'] - final_result['cumulative_burned']
        flow_type = "Inflationary" if net_flow > 0 else "Deflationary"
        st.metric("Net Token Flow", f"{net_flow:,.0f} VCOIN", f"{flow_type}")
    
    with col4:
        st.metric("Final Token Supply", f"{final_result['current_supply']:,.0f} VCOIN", 
                 f"{((final_result['current_supply'] / initial_result['current_supply']) - 1) * 100:+.1f}%")
    
    # Token Circulation Breakdown
    st.markdown("#### 🔄 Token Circulation Breakdown")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.metric("Staked Tokens", f"{final_result['staked_tokens']:,.0f} VCOIN", 
                 f"{final_result['staked_percentage']:.1f}% of supply")
    
    with col2:
        st.metric("Available for Content", f"{final_result['circulating_for_content']:,.0f} VCOIN", 
                 f"Content & NFT rewards")
    
    with col3:
        st.metric("Available for Trade", f"{final_result['circulating_for_trade']:,.0f} VCOIN", 
                 f"Market liquidity")
    
    with col4:
        st.metric("NFT & Content Pool", f"{final_result['circulating_for_nft']:,.0f} VCOIN", 
                 f"Creator economy")
    
    # User Growth & Retention (Net of Churn)
    st.markdown("#### 👥 User Growth Analysis (Net of Churn)")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.metric("Final Active Users", f"{final_result['daily_users']:,.0f}", 
                 f"{((final_result['daily_users'] / initial_result['daily_users']) - 1) * 100:+.1f}%")
    
    with col2:
        # Calculate average monthly net growth from all monthly data points
        monthly_data = [r for r in results if r['net_monthly_growth'] != 0]
        avg_net_growth = sum(r['net_monthly_growth'] for r in monthly_data) / max(1, len(monthly_data)) if monthly_data else 0
        st.metric("Avg Monthly Net Growth", f"{avg_net_growth:,.0f} users", 
                 f"After churn deduction")
    
    with col3:
        st.metric("User Retention Rate", f"{final_result['user_retention_rate']:.1f}%", 
                 f"Monthly retention")
    
    with col4:
        # Show acquisition vs churn balance
        acquisition_rate = params.get('monthly_acquisition_rate', 0) * 100
        churn_rate = params.get('monthly_churn_rate', 0) * 100
        net_growth_rate = acquisition_rate - churn_rate
        
        growth_color = "normal" if net_growth_rate > 0 else "inverse"
        st.metric("Net Monthly Growth Rate", f"{net_growth_rate:+.1f}%", 
                 f"Acquisition: {acquisition_rate:.1f}% | Churn: {churn_rate:.1f}%", 
                 delta_color=growth_color)
    
    # Platform Health & Economy Scores
    st.markdown("#### 🏥 Platform Health & Economy Scores")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        health_color = "normal" if final_result['platform_health'] > 70 else "inverse"
        st.metric("Platform Health", f"{final_result['platform_health']:.1f}/100", 
                 delta_color=health_color)
    
    with col2:
        economy_color = "normal" if final_result['token_economy_score'] > 70 else "inverse"
        st.metric("Economy Score", f"{final_result['token_economy_score']:.1f}/100", 
                 delta_color=economy_color)
    
    with col3:
        satisfaction_color = "normal" if final_result['user_satisfaction'] > 70 else "inverse"
        st.metric("User Satisfaction", f"{final_result['user_satisfaction']:.1f}/100", 
                 delta_color=satisfaction_color)
    
    with col4:
        # Calculate overall economy health (average of all scores)
        overall_health = (final_result['platform_health'] + final_result['token_economy_score'] + final_result['user_satisfaction']) / 3
        overall_color = "normal" if overall_health > 70 else "inverse"
        st.metric("Overall Economy Health", f"{overall_health:.1f}/100", 
                 delta_color=overall_color)
    
    # Economy Working Indicators
    st.markdown("#### ⚖️ Economy Working Indicators")
    
    # Determine if economy is working
    economy_working_score = 0
    indicators = []
    
    # Token price stability (25 points)
    price_change_abs = abs(final_result['total_value_change'])
    if price_change_abs < 20:
        economy_working_score += 25
        indicators.append("✅ Token price stable (< 20% change)")
    elif price_change_abs < 50:
        economy_working_score += 15
        indicators.append("⚠️ Token price moderately volatile (20-50% change)")
    else:
        indicators.append("❌ Token price highly volatile (> 50% change)")
    
    # User growth vs churn (25 points)
    if final_result['daily_users'] > initial_result['daily_users']:
        economy_working_score += 25
        indicators.append("✅ User base growing despite churn")
    else:
        indicators.append("❌ User base declining due to churn")
    
    # Token supply balance (25 points)
    burn_mint_ratio = final_result['cumulative_burned'] / max(1, final_result['cumulative_minted'])
    if 0.7 <= burn_mint_ratio <= 1.3:
        economy_working_score += 25
        indicators.append("✅ Healthy burn/mint ratio (0.7-1.3)")
    elif 0.5 <= burn_mint_ratio <= 1.5:
        economy_working_score += 15
        indicators.append("⚠️ Moderate burn/mint ratio (0.5-1.5)")
    else:
        indicators.append("❌ Unhealthy burn/mint ratio")
    
    # Platform sustainability (25 points)
    if final_result['revenue_cost_ratio'] > 1.2:
        economy_working_score += 25
        indicators.append("✅ Platform profitable (revenue > costs)")
    elif final_result['revenue_cost_ratio'] > 1.0:
        economy_working_score += 15
        indicators.append("⚠️ Platform break-even")
    else:
        indicators.append("❌ Platform losing money")
    
    # Display economy health verdict
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if economy_working_score >= 80:
            st.success(f"🎉 **Economy is WORKING!** ({economy_working_score}/100)")
        elif economy_working_score >= 60:
            st.warning(f"⚠️ **Economy is STABLE** ({economy_working_score}/100)")
        else:
            st.error(f"❌ **Economy NEEDS WORK** ({economy_working_score}/100)")
    
    with col2:
        st.markdown("**Key Indicators:**")
        for indicator in indicators:
            st.markdown(f"- {indicator}")
    
    # Content Calculator Alignment Section
    st.markdown("---")
    st.subheader("🎬 Content Calculator Alignment Check")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        per_content_reward = final_result.get('enhanced_reward_per_content', 0)
        st.metric("Per Content Reward", f"{per_content_reward:,.0f} VCOIN", 
                 f"${per_content_reward * final_result['token_price']:,.2f}")
    
    with col2:
        daily_content = final_result.get('daily_content_pieces', 0)
        st.metric("Daily Content Pieces", f"{daily_content:,.0f}", 
                 f"From {final_result['daily_creators']:,.0f} creators")
    
    with col3:
        total_multiplier = final_result.get('total_multiplier', 1.0)
        st.metric("Content Multiplier", f"{total_multiplier:.2f}x", 
                 f"Quality + Engagement boost")
    
    with col4:
        base_reward = final_result.get('base_reward_per_content', 0)
        st.metric("Base Reward per Content", f"{base_reward:,.0f} VCOIN", 
                 f"Before multipliers")
    
    # Explanation of alignment
    if final_result['platform_revenue'] > 0:
        reward_calculation = f"""
        **🔄 Revenue-Backed Calculation (90% to rewards):**
        - Daily Revenue: ${final_result['platform_revenue']:,.0f}
        - Reward Pool: ${final_result['platform_revenue'] * 0.90:,.0f} (90%)
        - Token Pool: {(final_result['platform_revenue'] * 0.90) / final_result['token_price']:,.0f} VCOIN
        - Content Pieces: {daily_content:,.0f}
        - Base per Content: {base_reward:,.0f} VCOIN
        - With Multipliers: {per_content_reward:,.0f} VCOIN
        """
    else:
        daily_mint = final_result.get('daily_minted', 0)
        reward_calculation = f"""
        **🚀 Bootstrap Mode Calculation (Token Minting):**
        - Daily Token Mint: {daily_mint:,.0f} VCOIN
        - Content Pieces: {daily_content:,.0f}
        - Base per Content: {base_reward:,.0f} VCOIN
        - With Multipliers: {per_content_reward:,.0f} VCOIN
        - **This matches Content Calculator bootstrap mode!**
        """
    
    st.info(reward_calculation)
    
    # Additional metrics row
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("Staked Tokens", f"{final_result['staked_percentage']:.1f}%")
    
    with col2:
        st.metric("Platform Health", f"{final_result['platform_health']:.1f}/100")
    
    with col3:
        st.metric("Economy Score", f"{final_result['token_economy_score']:.1f}/100")
    
    # Charts
    st.subheader("📈 Performance Charts")
    
    # Prepare data for charts
    days = [r['day'] for r in results]
    prices = [r['token_price'] for r in results]
    users = [r['daily_users'] for r in results]
    supply = [r['current_supply'] for r in results]
    
    # Price and user growth chart
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Token Price Over Time', 'User Growth', 'Token Supply', 'Daily Rewards'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(go.Scatter(x=days, y=prices, name="Token Price ($)", line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=days, y=users, name="Daily Users", line=dict(color='blue')), row=1, col=2)
    fig.add_trace(go.Scatter(x=days, y=supply, name="Token Supply", line=dict(color='orange')), row=2, col=1)
    fig.add_trace(go.Scatter(x=days, y=[r['total_rewards'] for r in results], name="Daily Rewards", line=dict(color='purple')), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=True, title_text="Economic Simulation Results")
    st.plotly_chart(fig, width="stretch")
    
    # Economic Health Metrics
    st.subheader("💊 Economic Health Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**🟢 Positive Indicators:**")
        if final_result['revenue_cost_ratio'] > 1:
            st.write("✅ Revenue covers costs")
        if final_result['user_retention_rate'] > 80:
            st.write("✅ Strong user retention")
        if final_result['staked_percentage'] > 30:
            st.write("✅ Good token staking rate")
        if final_result['acquisition_roi'] > 2:
            st.write("✅ Positive user acquisition ROI")
    
    with col2:
        st.markdown("**🔴 Risk Factors:**")
        if final_result['current_inflation_rate'] > 10:
            st.write("⚠️ High inflation rate")
        if final_result['user_retention_rate'] < 70:
            st.write("⚠️ High user churn")
        if final_result['revenue_cost_ratio'] < 1:
            st.write("⚠️ Costs exceed revenue")
        if final_result['token_price'] < initial_result['token_price'] * 0.5:
            st.write("⚠️ Significant token devaluation")
    
    # Detailed breakdown
    with st.expander("📋 Detailed Economic Breakdown"):
        st.markdown(f"""
        **Creator Economics:**
        - Daily creator rewards: {final_result['creator_rewards']:,.0f} VCOIN
        - Average creator earnings: ${final_result['avg_creator_earnings']:.2f}/day
        - Total creators: {final_result['daily_creators']:,.0f}
        
        **User Economics:**
        - Daily engagement rewards: {final_result['engagement_rewards']:,.0f} VCOIN
        - Average user earnings: ${final_result['avg_user_earnings']:.2f}/day
        - User retention rate: {final_result['user_retention_rate']:.1f}%
        
        **Platform Economics:**
        - Daily platform revenue: ${final_result['platform_revenue']:,.0f}
        - Transaction fees: ${final_result['transaction_fees']:,.0f}
        - User acquisition ROI: {final_result['acquisition_roi']:.1f}x
        
        **Token Economics:**
        - Current inflation: {final_result['current_inflation_rate']:.1f}% annually
        - Daily burn rate: {final_result['daily_burn_rate']:.2f}%
        - Token velocity: {final_result['actual_token_velocity']:.1f}x
        """)
    
    return results

def reverse_simulation_interface():
    """Reverse simulation to find optimal content-driven tokenomics parameters"""
    
    st.header("🔄 Reverse Simulation Calculator")
    st.markdown("**Work backwards from target earnings to find optimal content-driven tokenomics parameters**")
    
    # Content-driven target inputs
    st.subheader("🎯 Target Monthly Earnings")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        target_creator_monthly_usd = st.number_input(
            "Target Creator Monthly Earnings ($)", 
            value=1500.0, step=1.0,
            help="💡 How much should an average creator earn per month? (No limits - test any amount)"
        )
        
        target_posts_per_month = st.number_input(
            "Target Posts per Creator/Month",
            min_value=1, value=60, step=1,
            help="💡 Expected content output per creator monthly (2 posts/day = 60/month)"
        )
    
    with col2:
        target_consumer_monthly_usd = st.number_input(
            "Target Consumer Monthly Earnings ($)", 
            min_value=0.01, value=50.0, step=0.1,
            help="💡 How much should an average user earn monthly from engagement? (No upper limit)"
        )
        
        total_active_users = st.number_input(
            "Total App Active Users",
            min_value=1, value=100_000, step=1,
            help="💡 Total platform user base for calculations (No limits - test any scale)"
        )
    
    with col3:
        vcoin_price = st.number_input(
            "VCOIN Token Price ($)",
            min_value=0.0000001, max_value=10.0, value=0.10, step=0.01, format="%.7f",
            help="💡 Current VCOIN token price for calculations"
        )
    
    # Direct engagement input section
    st.subheader("📊 Content Engagement Metrics")
    st.markdown("**Input actual engagement numbers instead of platform assumptions**")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        total_monthly_views = st.number_input(
            "Total Monthly Views",
            min_value=1, value=10_000_000, step=1,
            help="💡 Total views across all content for the month (No limits)"
        )
    
    with col2:
        total_monthly_likes = st.number_input(
            "Total Monthly Likes",
            min_value=0, value=500_000, step=1,
            help="💡 Total likes across all content for the month (No limits)"
        )
    
    with col3:
        total_monthly_shares = st.number_input(
            "Total Monthly Shares",
            min_value=0, value=100_000, step=1,
            help="💡 Total shares/reposts across all content for the month (No limits)"
        )
    
    with col4:
        total_monthly_comments = st.number_input(
            "Total Monthly Comments",
            min_value=0, value=50_000, step=1,
            help="💡 Total comments across all content for the month (No limits)"
        )
        
    
    # Calculate engagement metrics
    total_monthly_engagement = total_monthly_likes + total_monthly_shares + total_monthly_comments
    monthly_engagement_rate = total_monthly_engagement / max(1, total_monthly_views)
    
    # Display engagement analysis
    st.info(f"""
    **📈 Engagement Analysis:**
    - Total Monthly Engagement: {total_monthly_engagement:,} interactions
    - Engagement Rate: {monthly_engagement_rate:.1%} of views
    - Views per Day: {total_monthly_views / 30:,.0f}
    - Engagement per Day: {total_monthly_engagement / 30:,.0f}
    """)
    
    # Calculate button
    if st.button("🧮 Calculate Content-Driven Parameters", type="primary", key="reverse_calc"):
        
        # Use direct engagement inputs for calculations
        assumed_token_price = vcoin_price
        
        # Calculate content and creator metrics based on actual data
        estimated_creators = int(total_active_users * 0.025)  # Assume 2.5% are creators
        total_monthly_posts = estimated_creators * target_posts_per_month
        daily_posts = total_monthly_posts / 30
        
        # Calculate required VCOIN per content to meet creator targets
        target_creator_daily_usd = target_creator_monthly_usd / 30
        target_consumer_daily_usd = target_consumer_monthly_usd / 30
        
        # Content-driven calculation
        creator_tokens_per_day = target_creator_daily_usd / assumed_token_price
        creator_posts_per_day = target_posts_per_month / 30
        
        # Calculate base VCOIN per content (creator gets 40% of content reward)
        required_vcoin_per_content = (creator_tokens_per_day / creator_posts_per_day) / 0.40
        
        # Calculate total minting needed (content-driven)
        total_daily_minting = daily_posts * required_vcoin_per_content
        
        # Calculate engagement distribution
        total_consumer_tokens_daily = target_consumer_daily_usd * total_active_users / assumed_token_price
        engagement_tokens_per_content = total_consumer_tokens_daily / daily_posts
        engagement_share_needed = engagement_tokens_per_content / required_vcoin_per_content
        
        # Calculate required burns for balance (target 70-80% burn rate)
        target_burn_rate = 0.75  # 75% of minting should be burned for balance
        required_daily_burns = total_daily_minting * target_burn_rate
        
        # Display results
        st.markdown("---")
        st.header("🎯 Content-Driven Tokenomics Parameters")
        
        # Content-driven minting parameters
        st.subheader("🪙 Required Content-Driven Minting")
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.metric("VCOIN per Content Piece", f"{required_vcoin_per_content:,.0f} VCOIN", 
                     f"${required_vcoin_per_content * assumed_token_price:,.2f}")
        
        with col2:
            st.metric("Daily Content Created", f"{daily_posts:,.0f} pieces", 
                     f"From {estimated_creators:,} creators")
        
        with col3:
            st.metric("Total Daily Minting", f"{total_daily_minting:,.0f} VCOIN", 
                     f"${total_daily_minting * assumed_token_price:,.0f}")
        
        with col4:
            monthly_minting = total_daily_minting * 30
            st.metric("Total Monthly Minting", f"{monthly_minting:,.0f} VCOIN", 
                     f"${monthly_minting * assumed_token_price:,.0f}")
        
        # Required burn mechanisms for balance
        st.subheader("🔥 Required Burn Mechanisms (30-Day Balance)")
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.metric("Required Daily Burns", f"{required_daily_burns:,.0f} VCOIN", 
                     f"{target_burn_rate:.0%} of minting")
        
        with col2:
            monthly_burns = required_daily_burns * 30
            st.metric("Required Monthly Burns", f"{monthly_burns:,.0f} VCOIN", 
                     f"For economic balance")
        
        with col3:
            net_monthly_flow = monthly_minting - monthly_burns
            st.metric("Net Monthly Token Flow", f"{net_monthly_flow:+,.0f} VCOIN", 
                     f"{'Inflationary' if net_monthly_flow > 0 else 'Deflationary'}")
        
        with col4:
            burn_efficiency = required_daily_burns / daily_posts
            st.metric("Burns per Content", f"{burn_efficiency:,.0f} VCOIN", 
                     f"Avg burn per content piece")
        
        # Content-driven economics breakdown
        st.subheader("📊 Content-Driven Economics Breakdown")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🎯 Creator Economics:**")
            creator_reward_per_content = required_vcoin_per_content * 0.40  # 40% to creator
            st.write(f"• Creators: {estimated_creators:,} (2.5% of users)")
            st.write(f"• Posts per Creator/Month: {target_posts_per_month}")
            st.write(f"• Creator Reward per Content: {creator_reward_per_content:,.0f} VCOIN")
            st.write(f"• Creator Monthly Earnings: {creator_reward_per_content * target_posts_per_month:,.0f} VCOIN")
            st.write(f"• Creator Monthly USD: ${creator_reward_per_content * target_posts_per_month * assumed_token_price:,.0f}")
            
            st.markdown("**🎮 Consumer Economics:**")
            consumer_reward_per_content = engagement_tokens_per_content
            st.write(f"• Consumers: {total_active_users - estimated_creators:,}")
            st.write(f"• Consumer Share per Content: {engagement_share_needed:.1%}")
            st.write(f"• Consumer Tokens per Content: {consumer_reward_per_content:,.2f} VCOIN")
            st.write(f"• Consumer Daily Earnings: {target_consumer_daily_usd * total_active_users / estimated_creators:,.2f} VCOIN")
            st.write(f"• Consumer Monthly USD: ${target_consumer_monthly_usd:,.0f}")
        
        with col2:
            st.markdown("**🪙 Token Minting Strategy:**")
            st.write(f"• Base Minting per Content: {required_vcoin_per_content:,.0f} VCOIN")
            st.write(f"• Daily Content Volume: {daily_posts:,.0f} pieces")
            st.write(f"• Daily Total Minting: {total_daily_minting:,.0f} VCOIN")
            st.write(f"• Monthly Total Minting: {monthly_minting:,.0f} VCOIN")
            st.write(f"• Minting tied to content creation: ✅")
            
            st.markdown("**🔥 Burn Requirements:**")
            st.write(f"• Target Burn Rate: {target_burn_rate:.0%} of minting")
            st.write(f"• Daily Burns Needed: {required_daily_burns:,.0f} VCOIN")
            st.write(f"• Monthly Burns Needed: {monthly_burns:,.0f} VCOIN")
            st.write(f"• Net Monthly Inflation: {(net_monthly_flow / monthly_minting) * 100:+.1f}%")
            st.write(f"• Economy Status: {'Balanced' if abs(net_monthly_flow / monthly_minting) < 0.3 else 'Needs Adjustment'}")
        
        # Implementation feasibility analysis
        st.markdown("---")
        st.subheader("🔍 Implementation Feasibility")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**💰 Economic Feasibility:**")
            minting_per_user_daily = total_daily_minting / total_active_users
            
            if required_vcoin_per_content > 5000:
                st.error("⚠️ **High Minting per Content**: Consider reducing target earnings or increasing content volume")
            elif required_vcoin_per_content < 500:
                st.warning("⚠️ **Low Minting per Content**: May not adequately incentivize creators")
            else:
                st.success("✅ **Balanced Minting per Content**: Sustainable and attractive to creators")
            
            st.write(f"• Daily Minting per User: {minting_per_user_daily:.1f} VCOIN")
            st.write(f"• Monthly Inflation Rate: {(net_monthly_flow / (total_active_users * 1000)) * 100:.2f}%")
            
        with col2:
            st.markdown("**🎯 Target Achievement:**")
            creator_achievement = (creator_reward_per_content * target_posts_per_month * assumed_token_price) / target_creator_monthly_usd
            consumer_achievement = (target_consumer_daily_usd * 30) / target_consumer_monthly_usd
            
            if creator_achievement >= 0.95:
                st.success(f"✅ Creator Target: {creator_achievement:.1%} achieved")
            else:
                st.warning(f"⚠️ Creator Target: Only {creator_achievement:.1%} achieved")
            
            if consumer_achievement >= 0.95:
                st.success(f"✅ Consumer Target: {consumer_achievement:.1%} achieved")
            else:
                st.warning(f"⚠️ Consumer Target: Only {consumer_achievement:.1%} achieved")
        
        # Key recommendations
        st.subheader("💡 Implementation Recommendations")
        
        recommendations = []
        
        if required_vcoin_per_content > 3000:
            recommendations.append("🔻 **Reduce minting per content** or increase content volume to lower inflation")
        
        if engagement_share_needed > 0.6:
            recommendations.append("⚖️ **High engagement share needed** - ensure sufficient user engagement")
        
        if net_monthly_flow / monthly_minting > 0.5:
            recommendations.append("🔥 **Increase burn mechanisms** to control inflation")
        
        if daily_posts < 10:
            recommendations.append("📈 **Increase content creation incentives** to reach target volume")
        
        if not recommendations:
            recommendations.append("✅ **Parameters look balanced** - ready for implementation!")
        
        for rec in recommendations:
            st.info(rec)
        
        # Platform earnings comparison
        st.markdown("---")
        st.subheader("💰 Platform Earnings Comparison")
        st.markdown("**How much would this same engagement earn on other platforms?**")
        
        # Define platform monetization data (2024-2025 averages)
        platform_monetization = {
            'youtube': {
                'cpm': 3.5,  # $3.50 per 1,000 views
                'creator_share': 0.55,  # 55% to creators
                'name': '📺 YouTube',
                'description': 'Long-form video, ad revenue sharing'
            },
            'tiktok': {
                'cpm': 0.8,  # $0.80 per 1,000 views (Creator Fund)
                'creator_share': 1.0,  # 100% to creators (simplified)
                'name': '🎵 TikTok',
                'description': 'Short-form video, Creator Fund'
            },
            'x_twitter': {
                'cpm': 1.2,  # $1.20 per 1,000 views (Creator Revenue Sharing)
                'creator_share': 0.70,  # 70% to creators
                'name': '🐦 X (Twitter)',
                'description': 'Text/media posts, revenue sharing'
            }
        }
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        platforms = ['youtube', 'tiktok', 'x_twitter']
        columns = [col1, col2, col3]
        
        for platform, col in zip(platforms, columns):
            with col:
                platform_data = platform_monetization[platform]
                
                # Calculate earnings for this platform
                monthly_revenue = (total_monthly_views / 1000) * platform_data['cpm']
                creator_earnings = monthly_revenue * platform_data['creator_share']
                creator_earnings_per_creator = creator_earnings / max(1, estimated_creators)
                
                st.markdown(f"**{platform_data['name']}**")
                st.write(f"*{platform_data['description']}*")
                st.write(f"• CPM: ${platform_data['cpm']:.2f}")
                st.write(f"• Creator Share: {platform_data['creator_share']:.0%}")
                st.write(f"• Monthly Revenue: ${monthly_revenue:,.0f}")
                st.write(f"• Creator Earnings: ${creator_earnings:,.0f}")
                st.write(f"• Per Creator: ${creator_earnings_per_creator:,.0f}/month")
                
                # Compare with ViWo target
                viwo_target = target_creator_monthly_usd
                comparison_ratio = creator_earnings_per_creator / viwo_target if viwo_target > 0 else 0
                
                if comparison_ratio >= 1.0:
                    st.success(f"✅ {comparison_ratio:.1f}× ViWo target")
                elif comparison_ratio >= 0.5:
                    st.warning(f"⚠️ {comparison_ratio:.1f}× ViWo target")
                else:
                    st.error(f"❌ {comparison_ratio:.1f}× ViWo target")
        
        # Summary comparison
        st.markdown("---")
        st.subheader("🏆 ViWo vs Traditional Platforms")
        
        # Calculate ViWo total monthly creator earnings
        viwo_total_creator_earnings = estimated_creators * target_creator_monthly_usd
        
        comparison_summary = []
        for platform in platforms:
            platform_data = platform_monetization[platform]
            monthly_revenue = (total_monthly_views / 1000) * platform_data['cpm']
            creator_earnings = monthly_revenue * platform_data['creator_share']
            
            comparison_summary.append({
                'Platform': platform_data['name'],
                'Total Creator Earnings': f"${creator_earnings:,.0f}",
                'Per Creator Earnings': f"${creator_earnings / max(1, estimated_creators):,.0f}",
                'vs ViWo Target': f"{(creator_earnings / max(1, estimated_creators)) / target_creator_monthly_usd:.1f}×"
            })
        
        # Add ViWo row
        comparison_summary.append({
            'Platform': '🪙 ViWo (Target)',
            'Total Creator Earnings': f"${viwo_total_creator_earnings:,.0f}",
            'Per Creator Earnings': f"${target_creator_monthly_usd:,.0f}",
            'vs ViWo Target': "1.0× (Target)"
        })
        
        comparison_df = pd.DataFrame(comparison_summary)
        st.table(comparison_df)
        
        # Key insights
        st.markdown("**💡 Key Platform Insights:**")
        
        youtube_earnings = (total_monthly_views / 1000) * 3.5 * 0.55 / max(1, estimated_creators)
        tiktok_earnings = (total_monthly_views / 1000) * 0.8 / max(1, estimated_creators)
        x_earnings = (total_monthly_views / 1000) * 1.2 * 0.70 / max(1, estimated_creators)
        
        best_platform = max([
            ('YouTube', youtube_earnings),
            ('TikTok', tiktok_earnings), 
            ('X', x_earnings)
        ], key=lambda x: x[1])
        
        st.info(f"""
        **📊 Platform Performance with Your Engagement:**
        - **Best Traditional Platform**: {best_platform[0]} (${best_platform[1]:,.0f}/creator/month)
        - **ViWo Target**: ${target_creator_monthly_usd:,.0f}/creator/month
        - **ViWo Advantage**: {target_creator_monthly_usd / best_platform[1]:.1f}× better than best traditional platform
        - **Required VCOIN per Content**: {required_vcoin_per_content:,.0f} VCOIN to achieve this advantage
        """)
        
        # Export functionality
        if st.button("📄 Export Reverse Simulation", key="export_reverse"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            export_content = f"""VCOIN REVERSE SIMULATION REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== TARGET EARNINGS ===
Target Creator Daily Earnings: ${target_creator_daily_usd}
Target Consumer Daily Earnings: ${target_consumer_daily_usd}
Expected Creator Participation: {expected_creators_percent}%

=== PLATFORM ASSUMPTIONS ===
Daily Active Users: {assumed_daily_users:,}
Assumed Token Price: ${assumed_token_price:.7f}
Creator/Consumer Ratio: {creator_engagement_ratio:.1f}x

=== REQUIRED PARAMETERS ===
Required Daily Revenue: ${required_daily_revenue:,.0f}
Revenue per User: ${revenue_per_user:.2f}
Total Daily Token Rewards: {total_daily_tokens_needed:,.0f} VCOIN

Creator Share Needed: {creator_share_needed:.1%}
Consumer Share Needed: {consumer_share_needed:.1%}
Remaining (Commission + Royalty): {1 - creator_share_needed - consumer_share_needed:.1%}

=== TOKEN DISTRIBUTION ===
Active Creators: {creators_count:,.0f}
Creator Tokens per Day: {total_creator_tokens_needed/creators_count:,.0f}
Consumer Tokens per Day: {total_consumer_tokens_needed/assumed_daily_users:.0f}

=== FEASIBILITY ASSESSMENT ===
Revenue Requirement: {"High" if revenue_per_user > 10 else "Moderate" if revenue_per_user > 1 else "Feasible"}
Creator Share: {"High" if creator_share_needed > 0.6 else "Balanced"}
Consumer Share: {"Low" if consumer_share_needed < 0.2 else "Adequate"}
"""
            
            st.download_button(
                label="📄 Download Reverse Simulation Report",
                data=export_content,
                file_name=f"vcoin_reverse_simulation_{timestamp}.txt",
                mime="text/plain",
                width="stretch"
            )

def cold_start_scenario_interface():
    """Cold start scenario with ICO tokens and pre-launch staking"""
    
    st.header("🚀 Cold Start Scenario Simulation")
    st.markdown("**Simulate platform launch with ICO tokens, pre-launch staking, and initial token price**")
    
    # ICO and Pre-launch parameters
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🪙 ICO & Token Setup")
        
        # Enhanced token price input
        st.markdown("**Initial Token Price ($)**")
        
        col1, col2 = st.columns([3, 1])
        common_prices = ["0.0000001", "0.00001", "0.0001", "0.001", "0.01", "0.05", "0.10"]
        
        with col1:
            dropdown_options = common_prices + ["Custom..."]
            selected_option = st.selectbox(
                "Select or enter ICO price:",
                dropdown_options,
                index=5,
                key="price_dropdown_cold"
            )
        
        with col2:
            if selected_option == "Custom...":
                custom_price = st.text_input("Custom:", value="0.05", key="custom_price_cold")
                try:
                    initial_token_price = float(custom_price)
                    if initial_token_price <= 0:
                        st.error("⚠️ Must be > 0")
                        initial_token_price = 0.05
                except ValueError:
                    st.error("⚠️ Invalid")
                    initial_token_price = 0.05
            else:
                initial_token_price = float(selected_option)
                st.write("")
        
        st.success(f"💰 ICO Price: ${initial_token_price:.7f}")
        
        ico_tokens_sold = st.number_input("ICO Tokens Sold (millions)", 
                                        min_value=1, max_value=1000, value=100, step=10,
                                        help="💡 Tokens sold during ICO") * 1_000_000
        
        ico_funds_raised = ico_tokens_sold * initial_token_price
        st.info(f"**ICO Funds Raised: ${ico_funds_raised:,.0f}**")
        
        pre_staked_percentage = st.slider("Pre-Launch Staking (%)", 
                                        min_value=10, max_value=80, value=40, step=5,
                                        help="💡 Percentage of ICO tokens staked before launch")
        
        pre_staked_tokens = ico_tokens_sold * (pre_staked_percentage / 100)
        
        st.subheader("🎯 Launch Parameters")
        launch_daily_users = st.number_input("Launch Day Active Users", 
                                           min_value=10, max_value=100_000, value=1_000, step=100,
                                           help="💡 Users on day 1 of platform launch")
        
        # Revenue mode selection
        st.markdown("**💰 Revenue Model**")
        revenue_mode = st.radio(
            "Choose reward funding source:",
            ["Bootstrap Mode (Token-Only)", "Revenue-Supported Mode"],
            help="💡 Bootstrap: Rewards from token minting only. Revenue-Supported: Mix of tokens + revenue"
        )
        
        if revenue_mode == "Revenue-Supported Mode":
            launch_daily_revenue = st.number_input("Launch Daily Revenue ($)", 
                                                 min_value=10, max_value=50_000, value=500, step=50,
                                                 help="💡 Platform revenue on day 1")
            revenue_to_rewards_percent = st.slider("Revenue to Rewards (%)", 
                                                 min_value=50, max_value=90, value=70, step=5,
                                                 help="💡 Percentage of revenue allocated to rewards")
        else:
            launch_daily_revenue = 0
            revenue_to_rewards_percent = 0
            
            # Bootstrap mode parameters
            st.markdown("**🪙 Bootstrap Token Allocation**")
            daily_token_mint_rate = st.slider("Daily Token Mint Rate (%)", 
                                            min_value=0.01, max_value=1.0, value=0.1, step=0.01,
                                            help="💡 Daily % of total supply minted for rewards")
            
            bootstrap_duration_days = st.number_input("Bootstrap Period (days)", 
                                                    min_value=30, max_value=365, value=90, step=30,
                                                    help="💡 Days to run on pure token rewards before revenue kicks in")
            
            st.info(f"""
            🚀 **Bootstrap Mode Configuration:**
            - **No external revenue required** for first {bootstrap_duration_days} days
            - **Daily mint**: {daily_token_mint_rate}% of total supply for rewards
            - **Sustainable**: Controlled inflation to bootstrap ecosystem
            - **Transition**: Can switch to revenue-supported after bootstrap period
            """)
    
    with col2:
        st.subheader("📈 Growth Projections")
        
        monthly_user_growth = st.slider("Monthly User Growth (%)", 
                                       min_value=5, max_value=100, value=25, step=5,
                                       help="💡 Expected monthly user growth rate")
        
        monthly_churn_rate = st.slider("Monthly Churn Rate (%)", 
                                     min_value=5, max_value=50, value=20, step=5,
                                     help="💡 Percentage of users who leave monthly")
        
        monthly_revenue_growth = st.slider("Monthly Revenue Growth (%)", 
                                         min_value=5, max_value=80, value=20, step=5,
                                         help="💡 Expected monthly revenue growth rate")
        
        simulation_months = st.selectbox("Simulation Period (months)", 
                                       [3, 6, 12, 18, 24], index=2,
                                       help="💡 How many months to simulate post-launch")
        
        st.subheader("💰 Economic Settings")
        creator_share = st.slider("Creator Share (%)", 
                                min_value=20, max_value=60, value=40, step=5)
        
        engagement_share = st.slider("Engagement Share (%)", 
                                   min_value=20, max_value=60, value=40, step=5)
        
        commission_share = st.slider("Commission Share (%)", 
                                   min_value=5, max_value=20, value=10, step=1)
        
        royalty_share = 100 - creator_share - engagement_share - commission_share
        if royalty_share < 0:
            st.error("⚠️ Total shares cannot exceed 100%")
            royalty_share = 0
        else:
            st.info(f"**Royalty Share: {royalty_share}%**")
    
    # Execute simulation
    if st.button("🚀 Simulate Cold Start", type="primary", key="cold_start_sim"):
        
        # Calculate monthly metrics
        results = []
        current_users = launch_daily_users
        current_revenue = launch_daily_revenue
        current_token_price = initial_token_price
        circulating_supply = ico_tokens_sold
        staked_tokens = pre_staked_tokens
        
        for month in range(simulation_months + 1):  # Include month 0 (launch)
            # Monthly user dynamics
            if month > 0:
                new_users_added = current_users * (monthly_user_growth / 100)
                users_churned = current_users * (monthly_churn_rate / 100)
                net_user_change = new_users_added - users_churned
                current_users = max(launch_daily_users * 0.1, current_users + net_user_change)  # Never go below 10% of launch
                
                # Revenue growth
                current_revenue = current_revenue * (1 + monthly_revenue_growth / 100)
            else:
                new_users_added = 0
                users_churned = 0
                net_user_change = 0
            
            # Daily economics
            daily_creators = current_users * 0.05  # Assume 5% create content
            
            # Calculate rewards based on mode
            if revenue_mode == "Bootstrap Mode (Token-Only)":
                # Bootstrap mode: rewards from token minting
                days_elapsed = month * 30
                if days_elapsed <= bootstrap_duration_days:
                    # Pure bootstrap mode
                    daily_token_mint = circulating_supply * (daily_token_mint_rate / 100)
                    daily_rewards_pool_tokens = daily_token_mint
                    daily_rewards_pool_usd = 0  # No USD backing
                else:
                    # Transition period - could add revenue here
                    daily_rewards_pool_tokens = circulating_supply * (daily_token_mint_rate / 100) * 0.5  # Reduced minting
                    daily_rewards_pool_usd = current_revenue * (revenue_to_rewards_percent / 100) if current_revenue > 0 else 0
            else:
                # Revenue-supported mode
                daily_rewards_pool_usd = current_revenue * (revenue_to_rewards_percent / 100)
                daily_rewards_pool_tokens = daily_rewards_pool_usd / current_token_price if current_token_price > 0 else 0
            
            # Distribute rewards
            creator_rewards_tokens = daily_rewards_pool_tokens * (creator_share / 100)
            engagement_rewards_tokens = daily_rewards_pool_tokens * (engagement_share / 100)
            commission_rewards_tokens = daily_rewards_pool_tokens * (commission_share / 100)
            
            # Update circulating supply if minting tokens
            if revenue_mode == "Bootstrap Mode (Token-Only)" and month * 30 <= bootstrap_duration_days:
                circulating_supply += daily_token_mint * 30  # Monthly increase
            
            # Token price calculation
            if revenue_mode == "Bootstrap Mode (Token-Only)":
                # In bootstrap mode, price is driven by utility and scarcity
                if month == 0:
                    # Start with ICO price
                    current_token_price = initial_token_price
                else:
                    # Price influenced by user growth and token supply inflation
                    user_growth_factor = current_users / launch_daily_users
                    supply_inflation_factor = circulating_supply / ico_tokens_sold
                    # Price grows with users but is diluted by supply increase
                    current_token_price = initial_token_price * (user_growth_factor / supply_inflation_factor) * 0.8
                
                market_cap = current_token_price * circulating_supply
            else:
                # Revenue-supported mode
                market_cap = current_revenue * 365 * 8  # 8x annual revenue
                current_token_price = market_cap / circulating_supply if circulating_supply > 0 else initial_token_price
            
            # Creator and consumer earnings in USD
            avg_creator_earnings_usd = (creator_rewards_tokens * current_token_price) / max(1, daily_creators)
            avg_consumer_earnings_usd = (engagement_rewards_tokens * current_token_price) / current_users
            
            # Staking dynamics
            staking_apy = 0.15  # 15% APY
            monthly_staking_rewards = staked_tokens * (staking_apy / 12)
            
            result = {
                'month': month,
                'daily_users': current_users,
                'new_users_added': new_users_added,
                'users_churned': users_churned,
                'net_user_change': net_user_change,
                'daily_revenue': current_revenue,
                'token_price': current_token_price,
                'market_cap': market_cap,
                'circulating_supply': circulating_supply,
                'staked_tokens': staked_tokens,
                'staked_percentage': (staked_tokens / circulating_supply) * 100,
                'creator_rewards_tokens': creator_rewards_tokens,
                'engagement_rewards_tokens': engagement_rewards_tokens,
                'avg_creator_earnings_usd': avg_creator_earnings_usd,
                'avg_consumer_earnings_usd': avg_consumer_earnings_usd,
                'monthly_staking_rewards': monthly_staking_rewards,
                'churn_rate': monthly_churn_rate if month > 0 else 0,
                'growth_rate': monthly_user_growth if month > 0 else 0,
                'revenue_mode': revenue_mode,
                'daily_token_mint': daily_token_mint if revenue_mode == "Bootstrap Mode (Token-Only)" else 0,
                'bootstrap_active': month * 30 <= bootstrap_duration_days if revenue_mode == "Bootstrap Mode (Token-Only)" else False
            }
            
            results.append(result)
        
        # Display results
        st.markdown("---")
        st.header("📊 Cold Start Simulation Results")
        
        final_result = results[-1]
        initial_result = results[0]
        
        # Key metrics
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.metric("Final Users", f"{final_result['daily_users']:,.0f}",
                     f"{((final_result['daily_users'] / initial_result['daily_users']) - 1) * 100:+.1f}%")
            st.metric("Final Token Price", f"${final_result['token_price']:.7f}",
                     f"{((final_result['token_price'] / initial_result['token_price']) - 1) * 100:+.1f}%")
        
        with col2:
            st.metric("Final Daily Revenue", f"${final_result['daily_revenue']:,.0f}",
                     f"{((final_result['daily_revenue'] / initial_result['daily_revenue']) - 1) * 100:+.1f}%")
            st.metric("Market Cap", f"${final_result['market_cap']:,.0f}")
        
        with col3:
            st.metric("Creator Daily Earnings", f"${final_result['avg_creator_earnings_usd']:.2f}")
            st.metric("Consumer Daily Earnings", f"${final_result['avg_consumer_earnings_usd']:.2f}")
        
        with col4:
            st.metric("Staked Tokens", f"{final_result['staked_percentage']:.1f}%")
            st.metric("ICO ROI", f"{((final_result['token_price'] / initial_token_price) - 1) * 100:+.1f}%")
        
        # Monthly breakdown table
        st.subheader("📋 Monthly Progress")
        
        df_results = pd.DataFrame(results)
        df_display = df_results[[
            'month', 'daily_users', 'new_users_added', 'users_churned', 
            'daily_revenue', 'token_price', 'avg_creator_earnings_usd', 'avg_consumer_earnings_usd'
        ]].copy()
        
        df_display.columns = [
            'Month', 'Daily Users', 'New Users', 'Churned Users', 
            'Daily Revenue ($)', 'Token Price ($)', 'Creator Earnings ($)', 'Consumer Earnings ($)'
        ]
        
        # Format the dataframe
        df_display['Daily Users'] = df_display['Daily Users'].apply(lambda x: f"{x:,.0f}")
        df_display['New Users'] = df_display['New Users'].apply(lambda x: f"{x:,.0f}")
        df_display['Churned Users'] = df_display['Churned Users'].apply(lambda x: f"{x:,.0f}")
        df_display['Daily Revenue ($)'] = df_display['Daily Revenue ($)'].apply(lambda x: f"${x:,.0f}")
        df_display['Token Price ($)'] = df_display['Token Price ($)'].apply(lambda x: f"${x:.7f}")
        df_display['Creator Earnings ($)'] = df_display['Creator Earnings ($)'].apply(lambda x: f"${x:.2f}")
        df_display['Consumer Earnings ($)'] = df_display['Consumer Earnings ($)'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(df_display, width="stretch")
        
        # Bootstrap Mode Explanation
        if revenue_mode == "Bootstrap Mode (Token-Only)":
            st.subheader("🚀 Bootstrap Mode Analysis")
            
            with st.expander("📊 Bootstrap Economics Explained", expanded=True):
                bootstrap_months = bootstrap_duration_days // 30
                total_tokens_minted = sum([r['daily_token_mint'] * 30 for r in results if r['bootstrap_active']])
                
                st.markdown(f"""
                ### **🪙 Token-Only Bootstrap Strategy**
                
                **Why Bootstrap Mode?**
                - **No Revenue Dependency**: Platform can launch and reward users without external revenue
                - **Community Building**: Incentivizes early adopters with token rewards
                - **Network Effects**: Users earn tokens that gain value as platform grows
                - **Sustainable Launch**: Controlled token minting prevents unsustainable cash burn
                
                **📈 Bootstrap Metrics:**
                - **Bootstrap Period**: {bootstrap_duration_days} days ({bootstrap_months} months)
                - **Daily Mint Rate**: {daily_token_mint_rate}% of total supply
                - **Total Tokens Minted**: {total_tokens_minted:,.0f} VCOIN during bootstrap
                - **Supply Inflation**: {((final_result['circulating_supply'] / ico_tokens_sold) - 1) * 100:.1f}% over {simulation_months} months
                
                **🎯 Economic Logic:**
                1. **Early Rewards**: Users get tokens for engagement when platform has no revenue
                2. **Value Creation**: As user base grows, token utility and demand increase
                3. **Price Discovery**: Token price reflects platform growth and user adoption
                4. **Transition Ready**: Can switch to revenue-supported rewards once monetization kicks in
                
                **⚖️ Sustainability Factors:**
                - **Controlled Inflation**: {daily_token_mint_rate}% daily mint rate prevents hyperinflation
                - **User Growth**: {((final_result['daily_users'] / launch_daily_users) - 1) * 100:+.1f}% user growth supports token demand
                - **Utility Value**: Tokens have real utility for platform features and governance
                - **Future Revenue**: Bootstrap period allows time to develop revenue streams
                
                **🔄 Transition Strategy:**
                After bootstrap period ({bootstrap_duration_days} days), the platform can:
                - Reduce token minting rate to {daily_token_mint_rate/2}%
                - Introduce revenue-backed rewards
                - Maintain hybrid model (tokens + revenue)
                - Implement token burns to control supply
                """)
                
                # Show bootstrap vs revenue comparison
                if simulation_months * 30 > bootstrap_duration_days:
                    bootstrap_results = [r for r in results if r['bootstrap_active']]
                    post_bootstrap_results = [r for r in results if not r['bootstrap_active'] and r['month'] > 0]
                    
                    if bootstrap_results and post_bootstrap_results:
                        avg_bootstrap_creator_earnings = sum([r['avg_creator_earnings_usd'] for r in bootstrap_results]) / len(bootstrap_results)
                        avg_post_creator_earnings = sum([r['avg_creator_earnings_usd'] for r in post_bootstrap_results]) / len(post_bootstrap_results)
                        
                        st.info(f"""
                        **📊 Bootstrap vs Post-Bootstrap Comparison:**
                        - **Bootstrap Period Creator Earnings**: ${avg_bootstrap_creator_earnings:.2f}/day average
                        - **Post-Bootstrap Creator Earnings**: ${avg_post_creator_earnings:.2f}/day average
                        - **Transition Impact**: {((avg_post_creator_earnings / avg_bootstrap_creator_earnings) - 1) * 100:+.1f}% change
                        """)
        
        # Export functionality
        if st.button("📄 Export Cold Start Report", key="export_cold_start"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            export_content = f"""VCOIN COLD START SCENARIO REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== ICO & LAUNCH SETUP ===
Initial Token Price: ${initial_token_price:.7f}
ICO Tokens Sold: {ico_tokens_sold:,} VCOIN
ICO Funds Raised: ${ico_funds_raised:,.0f}
Pre-Launch Staking: {pre_staked_percentage}% ({pre_staked_tokens:,.0f} tokens)

Launch Daily Users: {launch_daily_users:,}
Launch Daily Revenue: ${launch_daily_revenue:,}

=== GROWTH PARAMETERS ===
Monthly User Growth: {monthly_user_growth}%
Monthly Churn Rate: {monthly_churn_rate}%
Monthly Revenue Growth: {monthly_revenue_growth}%
Simulation Period: {simulation_months} months

=== REWARD DISTRIBUTION ===
Creator Share: {creator_share}%
Engagement Share: {engagement_share}%
Commission Share: {commission_share}%
Royalty Share: {royalty_share}%

=== FINAL RESULTS (Month {simulation_months}) ===
Final Daily Users: {final_result['daily_users']:,.0f}
Final Daily Revenue: ${final_result['daily_revenue']:,.0f}
Final Token Price: ${final_result['token_price']:.7f}
Final Market Cap: ${final_result['market_cap']:,.0f}

Creator Daily Earnings: ${final_result['avg_creator_earnings_usd']:.2f}
Consumer Daily Earnings: ${final_result['avg_consumer_earnings_usd']:.2f}
ICO Token ROI: {((final_result['token_price'] / initial_token_price) - 1) * 100:+.1f}%

=== MONTHLY BREAKDOWN ===
"""
            
            for result in results:
                export_content += f"""
Month {result['month']}:
- Users: {result['daily_users']:,.0f} (New: {result['new_users_added']:,.0f}, Churned: {result['users_churned']:,.0f})
- Revenue: ${result['daily_revenue']:,.0f}
- Token Price: ${result['token_price']:.7f}
- Creator Earnings: ${result['avg_creator_earnings_usd']:.2f}
- Consumer Earnings: ${result['avg_consumer_earnings_usd']:.2f}
"""
            
            st.download_button(
                label="📄 Download Cold Start Report",
                data=export_content,
                file_name=f"vcoin_cold_start_{timestamp}.txt",
                mime="text/plain",
                width="stretch"
            )

def governance_dao_interface():
    """Governance and DAO Economics Simulation"""
    
    st.header("🏛️ Governance & DAO Economics")
    st.markdown("**Simulate governance participation, voting power distribution, and DAO treasury management**")
    
    # Parameter inputs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗳️ Governance Parameters")
        
        total_voting_tokens = st.number_input("Total Voting Tokens", 
                                            min_value=1_000_000, max_value=10_000_000_000, value=1_000_000_000, step=1_000_000,
                                            help="💡 Total tokens eligible for governance voting")
        
        min_proposal_tokens = st.number_input("Min Tokens to Propose", 
                                            min_value=1_000, max_value=10_000_000, value=100_000, step=10_000,
                                            help="💡 Minimum tokens required to submit a governance proposal")
        
        quorum_percentage = st.slider("Quorum Required (%)", 
                                    min_value=5, max_value=50, value=15, step=5,
                                    help="💡 Minimum percentage of tokens that must vote for proposal to be valid")
        
        voting_period_days = st.slider("Voting Period (days)", 
                                     min_value=1, max_value=14, value=7, step=1,
                                     help="💡 How long voting remains open for each proposal")
        
        governance_reward_pool = st.number_input("Monthly Governance Rewards", 
                                               min_value=0, max_value=10_000_000, value=500_000, step=50_000,
                                               help="💡 Monthly token rewards for governance participation")
        
        st.subheader("👥 Participation Dynamics")
        
        voter_participation_rate = st.slider("Voter Participation Rate (%)", 
                                           min_value=5, max_value=80, value=25, step=5,
                                           help="💡 Percentage of eligible voters who typically participate")
        
        whale_concentration = st.slider("Top 10 Holders Control (%)", 
                                       min_value=10, max_value=80, value=35, step=5,
                                       help="💡 Percentage of voting power held by top 10 addresses")
        
        delegation_rate = st.slider("Token Delegation Rate (%)", 
                                   min_value=0, max_value=70, value=20, step=5,
                                   help="💡 Percentage of tokens delegated to active voters")
    
    with col2:
        st.subheader("🏦 DAO Treasury")
        
        initial_treasury_usd = st.number_input("Initial Treasury (USD)", 
                                             min_value=100_000, max_value=100_000_000, value=5_000_000, step=100_000,
                                             help="💡 Initial DAO treasury funds")
        
        monthly_treasury_inflow = st.number_input("Monthly Treasury Inflow (USD)", 
                                                min_value=10_000, max_value=5_000_000, value=200_000, step=10_000,
                                                help="💡 Monthly funds flowing into treasury (fees, revenue share)")
        
        development_budget_percent = st.slider("Development Budget (%)", 
                                             min_value=20, max_value=70, value=40, step=5,
                                             help="💡 Percentage of treasury allocated to development")
        
        marketing_budget_percent = st.slider("Marketing Budget (%)", 
                                           min_value=10, max_value=50, value=25, step=5,
                                           help="💡 Percentage of treasury allocated to marketing")
        
        community_budget_percent = st.slider("Community Programs (%)", 
                                           min_value=10, max_value=40, value=20, step=5,
                                           help="💡 Percentage for community incentives and programs")
        
        reserve_percent = 100 - development_budget_percent - marketing_budget_percent - community_budget_percent
        if reserve_percent < 0:
            st.error("⚠️ Budget allocations exceed 100%")
            reserve_percent = 0
        else:
            st.info(f"**Reserve Fund: {reserve_percent}%**")
        
        st.subheader("📊 Proposal Economics")
        
        proposals_per_month = st.slider("Proposals per Month", 
                                       min_value=1, max_value=20, value=5, step=1,
                                       help="💡 Expected number of governance proposals monthly")
        
        proposal_success_rate = st.slider("Proposal Success Rate (%)", 
                                        min_value=20, max_value=90, value=60, step=5,
                                        help="💡 Percentage of proposals that typically pass")
    
    # Execute simulation
    if st.button("🏛️ Simulate Governance", type="primary", key="governance_sim"):
        
        # Calculate governance metrics
        quorum_tokens_needed = total_voting_tokens * (quorum_percentage / 100)
        participating_tokens = total_voting_tokens * (voter_participation_rate / 100)
        whale_tokens = total_voting_tokens * (whale_concentration / 100)
        delegated_tokens = total_voting_tokens * (delegation_rate / 100)
        
        # Treasury calculations
        monthly_dev_budget = monthly_treasury_inflow * (development_budget_percent / 100)
        monthly_marketing_budget = monthly_treasury_inflow * (marketing_budget_percent / 100)
        monthly_community_budget = monthly_treasury_inflow * (community_budget_percent / 100)
        monthly_reserve = monthly_treasury_inflow * (reserve_percent / 100)
        
        # Governance economics
        reward_per_participating_token = governance_reward_pool / max(1, participating_tokens)
        monthly_proposals = proposals_per_month
        successful_proposals = monthly_proposals * (proposal_success_rate / 100)
        
        # Display results
        st.markdown("---")
        st.header("🏛️ Governance Simulation Results")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.metric("Quorum Threshold", f"{quorum_tokens_needed:,.0f} tokens")
            st.metric("Participating Tokens", f"{participating_tokens:,.0f}")
            st.metric("Quorum Achievement", f"{'✅ Likely' if participating_tokens >= quorum_tokens_needed else '❌ At Risk'}")
        
        with col2:
            st.metric("Whale Voting Power", f"{whale_concentration}%")
            st.metric("Delegated Tokens", f"{delegated_tokens:,.0f}")
            st.metric("Governance Centralization", f"{'⚠️ High' if whale_concentration > 50 else '✅ Moderate' if whale_concentration > 30 else '✅ Low'}")
        
        with col3:
            st.metric("Monthly Dev Budget", f"${monthly_dev_budget:,.0f}")
            st.metric("Monthly Marketing", f"${monthly_marketing_budget:,.0f}")
            st.metric("Monthly Community", f"${monthly_community_budget:,.0f}")
        
        with col4:
            st.metric("Reward per Token", f"{reward_per_participating_token:.4f} VCOIN")
            st.metric("Monthly Proposals", f"{monthly_proposals}")
            st.metric("Success Rate", f"{proposal_success_rate}%")
        
        # Governance health analysis
        st.subheader("🔍 Governance Health Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🟢 Positive Indicators:**")
            if participating_tokens >= quorum_tokens_needed:
                st.write("✅ Sufficient participation for quorum")
            if whale_concentration < 40:
                st.write("✅ Reasonable decentralization")
            if delegation_rate > 15:
                st.write("✅ Active delegation system")
            if proposal_success_rate > 40 and proposal_success_rate < 80:
                st.write("✅ Healthy proposal success rate")
        
        with col2:
            st.markdown("**🔴 Risk Factors:**")
            if participating_tokens < quorum_tokens_needed:
                st.write("⚠️ Low participation - quorum at risk")
            if whale_concentration > 50:
                st.write("⚠️ High centralization risk")
            if voter_participation_rate < 15:
                st.write("⚠️ Very low voter engagement")
            if proposal_success_rate > 85:
                st.write("⚠️ Potentially rubber-stamp governance")
        
        # Treasury projection
        st.subheader("💰 12-Month Treasury Projection")
        
        months = list(range(1, 13))
        treasury_balance = [initial_treasury_usd + (monthly_treasury_inflow - monthly_treasury_inflow) * month for month in months]
        treasury_balance = [initial_treasury_usd + monthly_reserve * month for month in months]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=treasury_balance, mode='lines+markers', 
                               name='Treasury Balance', line=dict(color='green', width=3)))
        fig.update_layout(title="DAO Treasury Growth", xaxis_title="Month", yaxis_title="Treasury Value (USD)")
        st.plotly_chart(fig, width="stretch")
        
        # Export functionality
        if st.button("📄 Export Governance Analysis", key="export_governance"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            export_content = f"""VCOIN GOVERNANCE & DAO ANALYSIS REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== GOVERNANCE PARAMETERS ===
Total Voting Tokens: {total_voting_tokens:,} VCOIN
Min Tokens to Propose: {min_proposal_tokens:,} VCOIN
Quorum Required: {quorum_percentage}%
Voting Period: {voting_period_days} days
Monthly Governance Rewards: {governance_reward_pool:,} VCOIN

=== PARTICIPATION DYNAMICS ===
Voter Participation Rate: {voter_participation_rate}%
Top 10 Holders Control: {whale_concentration}%
Token Delegation Rate: {delegation_rate}%
Participating Tokens: {participating_tokens:,.0f}
Quorum Threshold: {quorum_tokens_needed:,.0f}

=== DAO TREASURY ===
Initial Treasury: ${initial_treasury_usd:,}
Monthly Inflow: ${monthly_treasury_inflow:,}
Development Budget: {development_budget_percent}% (${monthly_dev_budget:,.0f}/month)
Marketing Budget: {marketing_budget_percent}% (${monthly_marketing_budget:,.0f}/month)
Community Budget: {community_budget_percent}% (${monthly_community_budget:,.0f}/month)
Reserve Fund: {reserve_percent}% (${monthly_reserve:,.0f}/month)

=== PROPOSAL ECONOMICS ===
Proposals per Month: {proposals_per_month}
Success Rate: {proposal_success_rate}%
Successful Proposals/Month: {successful_proposals:.1f}
Reward per Participating Token: {reward_per_participating_token:.4f} VCOIN

=== GOVERNANCE HEALTH ASSESSMENT ===
Quorum Achievement: {'Likely' if participating_tokens >= quorum_tokens_needed else 'At Risk'}
Centralization Risk: {'High' if whale_concentration > 50 else 'Moderate' if whale_concentration > 30 else 'Low'}
Participation Level: {'High' if voter_participation_rate > 30 else 'Moderate' if voter_participation_rate > 15 else 'Low'}
Treasury Sustainability: {'Growing' if monthly_reserve > 0 else 'Stable' if monthly_reserve == 0 else 'Declining'}

=== 12-MONTH TREASURY PROJECTION ===
Year-End Treasury: ${treasury_balance[-1]:,.0f}
Total Reserve Accumulated: ${monthly_reserve * 12:,.0f}
Monthly Burn Rate: ${monthly_treasury_inflow - monthly_reserve:,.0f}
"""
            
            st.download_button(
                label="📄 Download Governance Report",
                data=export_content,
                file_name=f"vcoin_governance_analysis_{timestamp}.txt",
                mime="text/plain",
                width="stretch"
            )

def vesting_unlocks_interface():
    """Token Vesting and Unlock Schedule Simulation"""
    
    st.header("📅 Vesting & Token Unlocks")
    st.markdown("**Simulate token vesting schedules, unlock events, and their market impact**")
    
    # Vesting parameters
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("👥 Stakeholder Allocations")
        
        total_token_supply = st.number_input("Total Token Supply", 
                                           min_value=1_000_000, max_value=50_000_000_000, value=10_000_000_000, step=1_000_000,
                                           help="💡 Total tokens to be distributed")
        
        team_allocation = st.slider("Team Allocation (%)", 
                                  min_value=5, max_value=30, value=15, step=1,
                                  help="💡 Tokens allocated to team members")
        
        investor_allocation = st.slider("Investor Allocation (%)", 
                                       min_value=10, max_value=50, value=25, step=1,
                                       help="💡 Tokens allocated to private investors")
        
        advisor_allocation = st.slider("Advisor Allocation (%)", 
                                     min_value=1, max_value=10, value=3, step=1,
                                     help="💡 Tokens allocated to advisors")
        
        community_allocation = st.slider("Community Allocation (%)", 
                                        min_value=20, max_value=70, value=40, step=1,
                                        help="💡 Tokens for community rewards and airdrops")
        
        treasury_allocation = st.slider("Treasury/Reserve (%)", 
                                       min_value=5, max_value=25, value=10, step=1,
                                       help="💡 Tokens held in treasury for future use")
        
        liquidity_allocation = 100 - team_allocation - investor_allocation - advisor_allocation - community_allocation - treasury_allocation
        if liquidity_allocation < 0:
            st.error("⚠️ Allocations exceed 100%")
            liquidity_allocation = 0
        else:
            st.info(f"**Liquidity/Public Sale: {liquidity_allocation}%**")
    
    with col2:
        st.subheader("⏰ Vesting Schedules")
        
        team_cliff_months = st.slider("Team Cliff Period (months)", 
                                    min_value=6, max_value=24, value=12, step=3,
                                    help="💡 Initial lock period before any team tokens unlock")
        
        team_vesting_months = st.slider("Team Vesting Duration (months)", 
                                       min_value=12, max_value=60, value=36, step=6,
                                       help="💡 Total time for team tokens to fully vest")
        
        investor_cliff_months = st.slider("Investor Cliff Period (months)", 
                                        min_value=0, max_value=12, value=6, step=3,
                                        help="💡 Initial lock period for investor tokens")
        
        investor_vesting_months = st.slider("Investor Vesting Duration (months)", 
                                           min_value=6, max_value=36, value=18, step=3,
                                           help="💡 Total time for investor tokens to fully vest")
        
        advisor_cliff_months = st.slider("Advisor Cliff Period (months)", 
                                        min_value=3, max_value=12, value=6, step=3,
                                        help="💡 Initial lock period for advisor tokens")
        
        advisor_vesting_months = st.slider("Advisor Vesting Duration (months)", 
                                         min_value=6, max_value=24, value=12, step=3,
                                         help="💡 Total time for advisor tokens to fully vest")
        
        st.subheader("💹 Market Impact")
        
        # Enhanced token price input
        st.markdown("**Token Price at TGE ($)**")
        
        col1, col2 = st.columns([3, 1])
        common_prices = ["0.0000001", "0.00001", "0.0001", "0.001", "0.01", "0.10", "1.00"]
        
        with col1:
            dropdown_options = common_prices + ["Custom..."]
            selected_option = st.selectbox(
                "Select or enter TGE price:",
                dropdown_options,
                index=5,
                key="price_dropdown_vesting"
            )
        
        with col2:
            if selected_option == "Custom...":
                custom_price = st.text_input("Custom:", value="0.10", key="custom_price_vesting")
                try:
                    initial_token_price = float(custom_price)
                    if initial_token_price <= 0:
                        st.error("⚠️ Must be > 0")
                        initial_token_price = 0.10
                except ValueError:
                    st.error("⚠️ Invalid")
                    initial_token_price = 0.10
            else:
                initial_token_price = float(selected_option)
                st.write("")
        
        st.success(f"💰 TGE Price: ${initial_token_price:.7f}")
        
        unlock_sell_pressure = st.slider("Unlock Sell Pressure (%)", 
                                        min_value=5, max_value=80, value=30, step=5,
                                        help="💡 Percentage of unlocked tokens typically sold immediately")
        
        market_absorption_rate = st.slider("Market Absorption Rate (%)", 
                                         min_value=10, max_value=100, value=70, step=10,
                                         help="💡 Market's ability to absorb selling without major price impact")
    
    # Simulation period
    simulation_months = st.selectbox("Simulation Period (months)", 
                                   [12, 24, 36, 48, 60], index=2,
                                   help="💡 How many months to simulate vesting")
    
    # Execute simulation
    if st.button("📅 Simulate Vesting Schedule", type="primary", key="vesting_sim"):
        
        # Calculate token amounts
        team_tokens = total_token_supply * (team_allocation / 100)
        investor_tokens = total_token_supply * (investor_allocation / 100)
        advisor_tokens = total_token_supply * (advisor_allocation / 100)
        community_tokens = total_token_supply * (community_allocation / 100)
        treasury_tokens = total_token_supply * (treasury_allocation / 100)
        liquidity_tokens = total_token_supply * (liquidity_allocation / 100)
        
        # Simulate monthly unlocks
        months = list(range(0, simulation_months + 1))
        monthly_unlocks = []
        circulating_supply = [liquidity_tokens + community_tokens * 0.1]  # Assume 10% community tokens at TGE
        token_price = [initial_token_price]
        
        for month in range(1, simulation_months + 1):
            monthly_unlock = 0
            
            # Team vesting
            if month > team_cliff_months:
                monthly_team_unlock = team_tokens / max(1, team_vesting_months - team_cliff_months)
                monthly_unlock += monthly_team_unlock
            
            # Investor vesting
            if month > investor_cliff_months:
                monthly_investor_unlock = investor_tokens / max(1, investor_vesting_months - investor_cliff_months)
                monthly_unlock += monthly_investor_unlock
            
            # Advisor vesting
            if month > advisor_cliff_months:
                monthly_advisor_unlock = advisor_tokens / max(1, advisor_vesting_months - advisor_cliff_months)
                monthly_unlock += monthly_advisor_unlock
            
            # Community gradual release (assume 5% per month)
            monthly_community_unlock = community_tokens * 0.05
            monthly_unlock += monthly_community_unlock
            
            monthly_unlocks.append(monthly_unlock)
            
            # Calculate circulating supply
            new_circulating = circulating_supply[-1] + monthly_unlock
            circulating_supply.append(new_circulating)
            
            # Calculate price impact
            sell_pressure = monthly_unlock * (unlock_sell_pressure / 100)
            price_impact = 1 - (sell_pressure / (circulating_supply[-1] * market_absorption_rate / 100))
            new_price = token_price[-1] * max(0.1, price_impact)  # Minimum 90% price drop protection
            token_price.append(new_price)
        
        # Display results
        st.markdown("---")
        st.header("📅 Vesting Simulation Results")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.metric("Initial Circulating", f"{circulating_supply[0]:,.0f}")
            st.metric("Final Circulating", f"{circulating_supply[-1]:,.0f}")
            st.metric("Total Unlocked", f"{circulating_supply[-1] - circulating_supply[0]:,.0f}")
        
        with col2:
            st.metric("Initial Price", f"${token_price[0]:.7f}")
            st.metric("Final Price", f"${token_price[-1]:.7f}")
            price_change = ((token_price[-1] / token_price[0]) - 1) * 100
            st.metric("Price Change", f"{price_change:+.1f}%")
        
        with col3:
            max_monthly_unlock = max(monthly_unlocks) if monthly_unlocks else 0
            st.metric("Peak Monthly Unlock", f"{max_monthly_unlock:,.0f}")
            avg_monthly_unlock = sum(monthly_unlocks) / len(monthly_unlocks) if monthly_unlocks else 0
            st.metric("Avg Monthly Unlock", f"{avg_monthly_unlock:,.0f}")
        
        with col4:
            total_unlock_value = sum(monthly_unlocks) * initial_token_price
            st.metric("Total Unlock Value", f"${total_unlock_value:,.0f}")
            dilution_rate = (circulating_supply[-1] / circulating_supply[0] - 1) * 100
            st.metric("Supply Dilution", f"{dilution_rate:.1f}%")
        
        # Vesting schedule chart
        st.subheader("📈 Token Unlock Schedule")
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Monthly Token Unlocks', 'Circulating Supply & Price Impact'),
            specs=[[{"secondary_y": False}], [{"secondary_y": True}]]
        )
        
        # Monthly unlocks
        fig.add_trace(
            go.Bar(x=months[1:], y=monthly_unlocks, name="Monthly Unlocks", marker_color='orange'),
            row=1, col=1
        )
        
        # Circulating supply
        fig.add_trace(
            go.Scatter(x=months, y=circulating_supply, name="Circulating Supply", line=dict(color='blue')),
            row=2, col=1
        )
        
        # Token price
        fig.add_trace(
            go.Scatter(x=months, y=token_price, name="Token Price", line=dict(color='red')),
            row=2, col=1, secondary_y=True
        )
        
        fig.update_layout(height=600, title_text="Vesting Schedule Analysis")
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Tokens", row=1, col=1)
        fig.update_yaxes(title_text="Circulating Supply", row=2, col=1)
        fig.update_yaxes(title_text="Price ($)", secondary_y=True, row=2, col=1)
        
        st.plotly_chart(fig, width="stretch")
        
        # Allocation breakdown
        st.subheader("🥧 Token Allocation Breakdown")
        
        labels = ['Team', 'Investors', 'Advisors', 'Community', 'Treasury', 'Liquidity/Public']
        values = [team_allocation, investor_allocation, advisor_allocation, 
                 community_allocation, treasury_allocation, liquidity_allocation]
        
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig_pie.update_layout(title="Token Distribution")
        st.plotly_chart(fig_pie, width="stretch")
        
        # Export functionality
        if st.button("📄 Export Vesting Analysis", key="export_vesting"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            export_content = f"""VCOIN VESTING & UNLOCK ANALYSIS REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== TOKEN ALLOCATION ===
Total Token Supply: {total_token_supply:,} VCOIN
Team Allocation: {team_allocation}% ({team_tokens:,.0f} tokens)
Investor Allocation: {investor_allocation}% ({investor_tokens:,.0f} tokens)
Advisor Allocation: {advisor_allocation}% ({advisor_tokens:,.0f} tokens)
Community Allocation: {community_allocation}% ({community_tokens:,.0f} tokens)
Treasury Allocation: {treasury_allocation}% ({treasury_tokens:,.0f} tokens)
Liquidity/Public: {liquidity_allocation}% ({liquidity_tokens:,.0f} tokens)

=== VESTING SCHEDULES ===
Team: {team_cliff_months} month cliff, {team_vesting_months} month vesting
Investors: {investor_cliff_months} month cliff, {investor_vesting_months} month vesting
Advisors: {advisor_cliff_months} month cliff, {advisor_vesting_months} month vesting

=== MARKET IMPACT PARAMETERS ===
Initial Token Price: ${initial_token_price:.7f}
Unlock Sell Pressure: {unlock_sell_pressure}%
Market Absorption Rate: {market_absorption_rate}%

=== SIMULATION RESULTS ({simulation_months} months) ===
Initial Circulating Supply: {circulating_supply[0]:,.0f} tokens
Final Circulating Supply: {circulating_supply[-1]:,.0f} tokens
Total Tokens Unlocked: {circulating_supply[-1] - circulating_supply[0]:,.0f} tokens
Supply Dilution: {dilution_rate:.1f}%

Price Impact:
Initial Price: ${token_price[0]:.7f}
Final Price: ${token_price[-1]:.7f}
Total Price Change: {price_change:+.1f}%

Unlock Metrics:
Peak Monthly Unlock: {max_monthly_unlock:,.0f} tokens
Average Monthly Unlock: {avg_monthly_unlock:,.0f} tokens
Total Unlock Value: ${total_unlock_value:,.0f}

=== MONTHLY BREAKDOWN ===
"""
            
            for i, month in enumerate(months[1:], 1):
                export_content += f"Month {month}: {monthly_unlocks[i-1]:,.0f} unlocked, {circulating_supply[month]:,.0f} circulating, ${token_price[month]:.7f} price\n"
            
            st.download_button(
                label="📄 Download Vesting Report",
                data=export_content,
                file_name=f"vcoin_vesting_analysis_{timestamp}.txt",
                mime="text/plain",
                width="stretch"
            )

def security_stress_test_interface():
    """Security and Economic Stress Testing"""
    
    st.header("🛡️ Security & Economic Stress Testing")
    st.markdown("**Test economic resilience against attacks, market crashes, and extreme scenarios**")
    
    # Stress test parameters
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Base Economic State")
        
        healthy_daily_users = st.number_input("Healthy Daily Users", 
                                            min_value=1_000, max_value=10_000_000, value=100_000, step=10_000,
                                            help="💡 Normal operating user count")
        
        healthy_daily_revenue = st.number_input("Healthy Daily Revenue ($)", 
                                               min_value=1_000, max_value=1_000_000, value=50_000, step=5_000,
                                               help="💡 Normal daily platform revenue")
        
        # Enhanced token price input
        st.markdown("**Healthy Token Price ($)**")
        
        col1, col2 = st.columns([3, 1])
        common_prices = ["0.0000001", "0.00001", "0.0001", "0.001", "0.01", "0.10", "1.00"]
        
        with col1:
            dropdown_options = common_prices + ["Custom..."]
            selected_option = st.selectbox(
                "Select or enter healthy price:",
                dropdown_options,
                index=5,
                key="price_dropdown_stress"
            )
        
        with col2:
            if selected_option == "Custom...":
                custom_price = st.text_input("Custom:", value="0.10", key="custom_price_stress")
                try:
                    healthy_token_price = float(custom_price)
                    if healthy_token_price <= 0:
                        st.error("⚠️ Must be > 0")
                        healthy_token_price = 0.10
                except ValueError:
                    st.error("⚠️ Invalid")
                    healthy_token_price = 0.10
            else:
                healthy_token_price = float(selected_option)
                st.write("")
        
        st.success(f"💰 Baseline: ${healthy_token_price:.7f}")
        
        circulating_supply = st.number_input("Circulating Supply", 
                                           min_value=1_000_000, max_value=10_000_000_000, value=1_000_000_000, step=1_000_000,
                                           help="💡 Current circulating token supply")
        
        st.subheader("⚡ Attack Scenarios")
        
        sybil_attack_scale = st.slider("Sybil Attack Scale", 
                                     min_value=1, max_value=10, value=3, step=1,
                                     help="💡 Scale of fake account creation (1=small, 10=massive)")
        
        whale_dump_percentage = st.slider("Whale Dump Size (%)", 
                                        min_value=1, max_value=50, value=15, step=1,
                                        help="💡 Percentage of circulating supply dumped by whale")
        
        spam_attack_multiplier = st.slider("Spam Attack Intensity", 
                                         min_value=1, max_value=20, value=5, step=1,
                                         help="💡 Multiplier of normal transaction volume")
        
        governance_attack_tokens = st.slider("Governance Attack Tokens (%)", 
                                           min_value=5, max_value=60, value=25, step=5,
                                           help="💡 Percentage of voting tokens controlled by attacker")
    
    with col2:
        st.subheader("📉 Market Stress Scenarios")
        
        bear_market_duration = st.slider("Bear Market Duration (months)", 
                                        min_value=3, max_value=24, value=12, step=3,
                                        help="💡 Length of sustained market downturn")
        
        market_crash_severity = st.slider("Market Crash Severity (%)", 
                                        min_value=30, max_value=95, value=70, step=5,
                                        help="💡 Percentage price drop during crash")
        
        user_exodus_rate = st.slider("User Exodus Rate (%)", 
                                    min_value=10, max_value=80, value=40, step=5,
                                    help="💡 Percentage of users leaving during crisis")
        
        revenue_decline_rate = st.slider("Revenue Decline Rate (%)", 
                                       min_value=20, max_value=90, value=60, step=5,
                                       help="💡 Revenue drop during stress period")
        
        st.subheader("🛡️ Defense Mechanisms")
        
        slashing_enabled = st.checkbox("Enable Slashing", value=True,
                                      help="💡 Penalize malicious behavior by destroying tokens")
        
        slashing_percentage = st.slider("Slashing Rate (%)", 
                                       min_value=1, max_value=100, value=30, step=5,
                                       help="💡 Percentage of tokens slashed for bad behavior")
        
        emergency_pause = st.checkbox("Emergency Pause Available", value=True,
                                     help="💡 Ability to pause certain functions during attacks")
        
        reputation_system = st.checkbox("Reputation System Active", value=True,
                                       help="💡 Track user reputation to limit new account abuse")
        
        minimum_stake_required = st.number_input("Minimum Stake to Participate", 
                                                min_value=0, max_value=10000, value=100, step=50,
                                                help="💡 Minimum tokens required to participate in rewards")
    
    # Execute stress tests
    if st.button("🛡️ Run Stress Tests", type="primary", key="stress_test"):
        
        # Calculate baseline metrics
        baseline_market_cap = healthy_daily_users * healthy_token_price * circulating_supply / healthy_daily_users
        baseline_tvl = healthy_daily_revenue * 365 * 5  # 5x revenue multiple
        
        # Stress test results
        st.markdown("---")
        st.header("🛡️ Stress Test Results")
        
        # Attack resistance analysis
        st.subheader("⚡ Attack Resistance Analysis")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown("**🎯 Sybil Attack Resistance**")
            sybil_cost = sybil_attack_scale * minimum_stake_required * healthy_token_price
            sybil_resistance = "High" if minimum_stake_required > 50 and reputation_system else "Medium" if minimum_stake_required > 10 else "Low"
            st.metric("Attack Cost", f"${sybil_cost:,.0f}")
            st.metric("Resistance Level", sybil_resistance)
            
            if reputation_system:
                st.write("✅ Reputation system active")
            if minimum_stake_required > 50:
                st.write("✅ High stake requirement")
        
        with col2:
            st.markdown("**🐋 Whale Dump Impact**")
            dump_tokens = circulating_supply * (whale_dump_percentage / 100)
            price_impact = whale_dump_percentage * 1.5  # Assume 1.5x price impact
            new_price = healthy_token_price * (1 - price_impact / 100)
            recovery_time = whale_dump_percentage / 2  # Rough estimate in days
            
            st.metric("Tokens Dumped", f"{dump_tokens:,.0f}")
            st.metric("Price Impact", f"-{price_impact:.1f}%")
            st.metric("New Price", f"${new_price:.7f}")
            st.metric("Recovery Time", f"~{recovery_time:.0f} days")
        
        with col3:
            st.markdown("**🏛️ Governance Attack**")
            attack_tokens = circulating_supply * (governance_attack_tokens / 100)
            attack_cost = attack_tokens * healthy_token_price
            governance_risk = "Critical" if governance_attack_tokens > 50 else "High" if governance_attack_tokens > 30 else "Moderate"
            
            st.metric("Attack Tokens", f"{attack_tokens:,.0f}")
            st.metric("Attack Cost", f"${attack_cost:,.0f}")
            st.metric("Risk Level", governance_risk)
        
        # Market stress analysis
        st.subheader("📉 Market Stress Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🐻 Bear Market Impact**")
            
            # Calculate progressive decline
            months = list(range(bear_market_duration + 1))
            user_decline = [healthy_daily_users * (1 - user_exodus_rate/100 * month/bear_market_duration) for month in months]
            revenue_decline = [healthy_daily_revenue * (1 - revenue_decline_rate/100 * month/bear_market_duration) for month in months]
            price_decline = [healthy_token_price * (1 - market_crash_severity/100 * month/bear_market_duration) for month in months]
            
            st.metric("Final Users", f"{user_decline[-1]:,.0f}")
            st.metric("Final Revenue", f"${revenue_decline[-1]:,.0f}")
            st.metric("Final Price", f"${price_decline[-1]:.7f}")
            
            # Recovery analysis
            recovery_months = bear_market_duration * 1.5
            st.metric("Est. Recovery Time", f"{recovery_months:.0f} months")
        
        with col2:
            st.markdown("**🛡️ Defense Effectiveness**")
            
            defense_score = 0
            if slashing_enabled:
                defense_score += 25
                st.write("✅ Slashing mechanism active")
            if emergency_pause:
                defense_score += 20
                st.write("✅ Emergency pause available")
            if reputation_system:
                defense_score += 25
                st.write("✅ Reputation system active")
            if minimum_stake_required > 50:
                defense_score += 30
                st.write("✅ High minimum stake")
            
            st.metric("Defense Score", f"{defense_score}/100")
            
            if defense_score >= 80:
                st.success("🛡️ Strong defense mechanisms")
            elif defense_score >= 60:
                st.warning("⚠️ Moderate defense mechanisms")
            else:
                st.error("❌ Weak defense mechanisms")
        
        # Economic resilience chart
        st.subheader("📊 Economic Resilience Over Time")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('User Base Stress Test', 'Revenue Stress Test', 'Token Price Stress Test', 'Recovery Projection'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(go.Scatter(x=months, y=user_decline, name="Users", line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=months, y=revenue_decline, name="Revenue", line=dict(color='green')), row=1, col=2)
        fig.add_trace(go.Scatter(x=months, y=price_decline, name="Price", line=dict(color='red')), row=2, col=1)
        
        # Recovery projection
        recovery_months_list = list(range(bear_market_duration, bear_market_duration + int(recovery_months)))
        recovery_multiplier = [(month - bear_market_duration) / recovery_months for month in recovery_months_list]
        price_recovery = [price_decline[-1] + (healthy_token_price - price_decline[-1]) * mult for mult in recovery_multiplier]
        
        fig.add_trace(go.Scatter(x=recovery_months_list, y=price_recovery, name="Price Recovery", 
                               line=dict(color='orange', dash='dash')), row=2, col=2)
        
        fig.update_layout(height=600, title_text="Economic Stress Test Results")
        st.plotly_chart(fig, width="stretch")
        
        # Export functionality
        if st.button("📄 Export Stress Test Report", key="export_stress_test"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            export_content = f"""VCOIN SECURITY & STRESS TEST REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== BASELINE METRICS ===
Healthy Daily Users: {healthy_daily_users:,}
Healthy Daily Revenue: ${healthy_daily_revenue:,}
Healthy Token Price: ${healthy_token_price:.7f}
Circulating Supply: {circulating_supply:,} VCOIN

=== ATTACK SCENARIOS ===
Sybil Attack:
- Scale: {sybil_attack_scale}/10
- Estimated Cost: ${sybil_cost:,.0f}
- Resistance Level: {sybil_resistance}

Whale Dump Attack:
- Dump Size: {whale_dump_percentage}% ({dump_tokens:,.0f} tokens)
- Price Impact: -{price_impact:.1f}%
- New Price: ${new_price:.7f}
- Recovery Time: ~{recovery_time:.0f} days

Governance Attack:
- Attack Tokens: {governance_attack_tokens}% ({attack_tokens:,.0f} tokens)
- Attack Cost: ${attack_cost:,.0f}
- Risk Level: {governance_risk}

=== MARKET STRESS TEST ===
Bear Market Duration: {bear_market_duration} months
Market Crash Severity: {market_crash_severity}%
User Exodus Rate: {user_exodus_rate}%
Revenue Decline Rate: {revenue_decline_rate}%

Final Impact:
- Users: {user_decline[-1]:,.0f} ({((user_decline[-1]/healthy_daily_users)-1)*100:+.1f}%)
- Revenue: ${revenue_decline[-1]:,.0f} ({((revenue_decline[-1]/healthy_daily_revenue)-1)*100:+.1f}%)
- Price: ${price_decline[-1]:.7f} ({((price_decline[-1]/healthy_token_price)-1)*100:+.1f}%)

=== DEFENSE MECHANISMS ===
Slashing Enabled: {'Yes' if slashing_enabled else 'No'}
Slashing Rate: {slashing_percentage}%
Emergency Pause: {'Available' if emergency_pause else 'Not Available'}
Reputation System: {'Active' if reputation_system else 'Inactive'}
Minimum Stake: {minimum_stake_required} VCOIN
Defense Score: {defense_score}/100

=== RESILIENCE ASSESSMENT ===
Attack Resistance: {sybil_resistance}
Market Stress Tolerance: {'High' if defense_score >= 80 else 'Medium' if defense_score >= 60 else 'Low'}
Recovery Time: {recovery_months:.0f} months
Overall Risk Level: {'Low' if defense_score >= 80 and sybil_resistance == 'High' else 'Medium' if defense_score >= 60 else 'High'}

=== RECOMMENDATIONS ===
"""
            
            if defense_score < 60:
                export_content += "- Strengthen defense mechanisms (slashing, reputation system)\n"
            if minimum_stake_required < 50:
                export_content += "- Increase minimum stake requirements\n"
            if governance_attack_tokens > 30:
                export_content += "- Implement governance safeguards against centralization\n"
            if whale_dump_percentage > 20:
                export_content += "- Consider anti-whale mechanisms or gradual unlock schedules\n"
            
            st.download_button(
                label="📄 Download Stress Test Report",
                data=export_content,
                file_name=f"vcoin_stress_test_{timestamp}.txt",
                mime="text/plain",
                width="stretch"
            )

def parameter_testing_interface():
    """Enhanced parameter testing interface with realistic validation and comprehensive parameters"""
    
    st.header("🎛️ Economic Parameter Testing")
    st.markdown("**Adjust tokenomics parameters and run comprehensive economic simulations**")
    
    # Parameter explanations
    with st.expander("📚 Parameter Importance & Guidelines"):
        st.markdown("""
        ### 🎯 Why These Parameters Matter:
        
        **Platform Metrics:**
        - **Daily Active Users**: Core engagement metric - drives token demand and transaction volume
        - **Daily Revenue**: Platform sustainability - must cover rewards and operational costs
        - **User Acquisition Cost**: Essential for growth planning and ROI calculations
        - **Monthly Acquisition Rate**: How many new users you gain each month (% of current base)
        - **Monthly Churn Rate**: How many users leave each month - impacts retention and token value
        
        **Economic Controls:**
        - **Transaction Fees**: Revenue generation and spam prevention mechanism
        - **Staking Rewards**: Incentivizes holding, reduces circulating supply
        - **Commission Burn Rate**: Deflationary pressure to maintain token value
        - **Inflation Rate**: Controls new token creation and supply expansion
        
        **User Behavior:**
        - **Average Session Duration**: Higher engagement = more earning opportunities
        - **Content Creation Rate**: Drives creator rewards and platform growth
        - **Token Velocity**: How fast tokens circulate - affects price stability
        
        ### 📊 Realistic Ranges:
        - **Testing/MVP**: 10-1K DAU, $10-100 daily revenue
        - **Small Platform**: 1K-10K DAU, $100-1K daily revenue
        - **Medium Platform**: 10K-100K DAU, $1K-10K daily revenue  
        - **Large Platform**: 100K+ DAU, $10K+ daily revenue
        
        ### 🧪 Testing Tips:
        - Start with small numbers (10-50 users, $20-50 revenue) to test mechanics
        - Scale up gradually to see economic behavior at different sizes
        - Very small numbers help understand per-user economics clearly
        """)
    
    # Create columns for parameter inputs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Platform Metrics")
        
        # Daily Active Users with flexible validation
        daily_users = st.number_input("Daily Active Users", 
                                     min_value=1, max_value=50_000_000, value=10_000, step=1,
                                     help="💡 Start small (10-100 for testing, 1K-10K for MVP, scale to millions for mature platforms)")
        
        # Daily Revenue with flexible validation
        daily_revenue = st.number_input("Daily Revenue ($)", 
                                       min_value=1, max_value=5_000_000, value=1_000, step=1,
                                       help="💡 Should be 2-5x daily token rewards for sustainability (can start as low as $10-50 for testing)")
        
        # User Acquisition Cost
        user_acquisition_cost = st.number_input("User Acquisition Cost ($)", 
                                               min_value=0.10, max_value=500.0, value=5.0, step=0.50,
                                               help="💡 Cost to acquire each new user through marketing")
        
        # User Growth & Churn Parameters
        st.markdown("**👥 User Growth & Retention:**")
        
        monthly_acquisition_rate = st.slider("Monthly User Acquisition Rate (%)", 
                                            min_value=0, max_value=100, value=20, step=1,
                                            help="💡 Percentage of current user base acquired as NEW users each month. Example: 20% means if you have 1000 users, you acquire 200 new users monthly")
        
        monthly_churn_rate = st.slider("Monthly Churn Rate (%)", 
                                      min_value=1, max_value=50, value=15, step=1,
                                      help="💡 Percentage of existing users who LEAVE the platform each month (5-20% is typical for social platforms)")
        
        # Average Session Duration
        avg_session_minutes = st.number_input("Average Session Duration (minutes)", 
                                            min_value=1, max_value=180, value=25, step=5,
                                            help="💡 Longer sessions = more engagement = more rewards earned")
        
        st.subheader("🎯 Reward Distribution")
        creator_share = st.slider("Creator Share (%)", 
                                 min_value=20, max_value=60, value=40, step=5,
                                 help="💡 Percentage of daily reward pool for content creators")
        
        engagement_share = st.slider("Engagement Share (%)", 
                                    min_value=20, max_value=60, value=40, step=5,
                                    help="💡 Rewards for likes, shares, comments, and consumption")
        
        commission_share = st.slider("Commission Share (%)", 
                                    min_value=5, max_value=20, value=10, step=1,
                                    help="💡 Platform fee - should cover operational costs")
        
        # Calculate royalty share (remaining percentage)
        royalty_share = 100 - creator_share - engagement_share - commission_share
        if royalty_share < 0:
            st.error("⚠️ Total shares cannot exceed 100%. Please adjust the values.")
            royalty_share = 0
        else:
            st.info(f"**Royalty Share (auto-calculated): {royalty_share}%** - NFT trading and content ownership")
    
    with col2:
        st.subheader("💰 Economic Controls")
        
        # Transaction Fees
        transaction_fee_percent = st.slider("Transaction Fee (%)", 
                                          min_value=0.1, max_value=5.0, value=1.0, step=0.1,
                                          help="💡 Fee on token transfers - generates revenue and prevents spam")
        
        # Staking Rewards
        staking_apy = st.slider("Staking APY (%)", 
                               min_value=5, max_value=50, value=15, step=5,
                               help="💡 Annual percentage yield for staked tokens - incentivizes holding")
        
        # Commission Burn Rate
        commission_burn_rate = st.slider("Commission Burn Rate (%)", 
                                        min_value=10, max_value=100, value=50, step=10,
                                        help="💡 Percentage of commission burned - creates deflationary pressure")
        
        # Inflation Rate
        annual_inflation_rate = st.slider("Annual Inflation Rate (%)", 
                                         min_value=1, max_value=20, value=8, step=1,
                                         help="💡 New token creation rate - should decrease over time")
        
        st.subheader("🪙 Token Supply & Pricing")
        
        # Enhanced token price input with editable dropdown
        st.markdown("**Starting Token Price ($)**")
        
        # Create a list of common values for the dropdown
        common_prices = ["0.0000001", "0.00001", "0.0001", "0.001", "0.01", "0.10", "1.00"]
        
        # Use selectbox with option to add custom value
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Add "Custom..." option to the list
            dropdown_options = common_prices + ["Custom..."]
            selected_option = st.selectbox(
                "Select or enter token price:",
                dropdown_options,
                index=5,  # Default to 0.10
                help="💡 Select a common price or choose 'Custom...' to enter your own value",
                key="price_dropdown_param"
            )
        
        with col2:
            if selected_option == "Custom...":
                custom_price = st.text_input(
                    "Custom Price:",
                    value="0.10",
                    key="custom_price_param",
                    help="Enter exact value"
                )
                try:
                    initial_token_price = float(custom_price)
                    if initial_token_price <= 0:
                        st.error("⚠️ Must be > 0")
                        initial_token_price = 0.10
                    elif initial_token_price > 100:
                        st.warning("⚠️ Very high price")
                except ValueError:
                    st.error("⚠️ Invalid number")
                    initial_token_price = 0.10
            else:
                initial_token_price = float(selected_option)
                st.write("") # Empty space for alignment
        
        # Show selected price
        st.success(f"💰 Token Price: ${initial_token_price:.7f}")
        
        # Quick add custom values to dropdown (for future use)
        if selected_option == "Custom..." and 'custom_price_param' in st.session_state:
            custom_val = st.session_state.custom_price_param
            if custom_val and custom_val not in common_prices:
                if st.button("💾 Save this price for quick access", key="save_price_param"):
                    st.success(f"Price ${custom_val} saved! (Note: Will be available in next session)")
                    # In a real app, you'd save this to a config file or database
        
        initial_supply = st.number_input("Initial Supply (millions)", 
                                        min_value=100, max_value=5000, value=1000, step=100,
                                        help="💡 Starting token supply at launch") * 1_000_000
        
        max_supply = st.number_input("Max Supply (millions)", 
                                    min_value=1000, max_value=50000, value=10000, step=1000,
                                    help="💡 Maximum tokens that will ever exist") * 1_000_000
        
        st.subheader("👥 User Behavior")
        
        # Content Creation Rate
        content_creation_rate = st.slider("Daily Content Creation Rate (%)", 
                                         min_value=1, max_value=20, value=5, step=1,
                                         help="💡 Percentage of DAU who create content daily")
        
        # Token Velocity
        token_velocity = st.slider("Token Velocity (annual)", 
                                  min_value=2, max_value=50, value=12, step=2,
                                  help="💡 How many times tokens change hands per year (lower = more holding)")
        
        st.subheader("🎮 Simulation Settings")
        simulation_months = st.selectbox("Simulation Period (months)", 
                                       [1, 3, 6, 12, 24], index=2,
                                       help="💡 How many months to simulate the economy")
        
        scenario_type = st.selectbox("Growth Scenario", 
                                   ["Conservative", "Moderate", "Aggressive"],
                                   help="💡 User and revenue growth trajectory")
    
    # Execute buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        execute_simulation = st.button("🚀 Execute Simulation", type="primary", width="stretch", key="simulation_execute")
    
    with col2:
        export_results = st.button("📄 Export Results", width="stretch", key="simulation_export")
    
    with col3:
        reset_defaults = st.button("🔄 Reset to Defaults", width="stretch", key="simulation_reset")
    
    # Reset functionality
    if reset_defaults:
        st.rerun()
    
    # Smart validation warnings (only for realistic scale platforms)
    if daily_users > 1000 and daily_revenue < (daily_users * 0.01):
        st.warning("⚠️ Daily revenue seems low compared to user base. Consider increasing revenue or decreasing users.")
    
    if daily_users > 100 and user_acquisition_cost > (daily_revenue / daily_users * 30):
        st.warning("⚠️ User acquisition cost is high compared to revenue per user. This may impact profitability.")
    
    # Helpful guidance for small numbers
    if daily_users < 100:
        st.info("💡 **Testing Mode**: Small user numbers are great for testing tokenomics mechanics!")
    
    if daily_revenue < 100:
        st.info("💡 **Early Stage**: Low revenue is normal for MVP testing and early-stage platforms.")
    
    # Token price impact guidance
    if initial_token_price < 0.001:
        st.info("💡 **Micro Token**: Ultra-low price enables high token rewards with small USD amounts.")
    elif initial_token_price > 1.0:
        st.warning("⚠️ **High-Value Token**: High price means fewer tokens distributed - ensure reward amounts are sufficient.")
    
    # Calculate daily token rewards estimate
    estimated_daily_tokens = (daily_revenue * 0.7) / initial_token_price  # 70% of revenue to rewards
    st.info(f"💰 **Estimated Daily Token Rewards**: {estimated_daily_tokens:,.0f} VCOIN (based on {initial_token_price:.7f} price)")
    
    # Main simulation execution
    if execute_simulation or 'simulation_executed' not in st.session_state:
        st.session_state.simulation_executed = True
        
        # Collect all parameters
        params = {
            'initial_supply': initial_supply,
            'max_supply': max_supply,
            'creator_share': creator_share / 100,  # Convert to decimal
            'engagement_share': engagement_share / 100,
            'commission_share': commission_share / 100,
            'royalty_share': royalty_share / 100,
            'commission_burn_rate': commission_burn_rate / 100,
            'transaction_fee_percent': transaction_fee_percent / 100,
            'staking_apy': staking_apy / 100,
            'annual_inflation_rate': annual_inflation_rate / 100,
            'monthly_churn_rate': monthly_churn_rate / 100,
            'monthly_acquisition_rate': monthly_acquisition_rate / 100,
            'content_creation_rate': content_creation_rate / 100,
            'daily_revenue': daily_revenue,
            'daily_users': daily_users,
            'user_acquisition_cost': user_acquisition_cost,
            'avg_session_minutes': avg_session_minutes,
            'token_velocity': token_velocity,
            'initial_price': initial_token_price  # User-specified starting price
        }
        
        # Convert months to days for simulation
        simulation_days = simulation_months * 30
        
        # Run simulation
        with st.spinner(f"🔄 Running {simulation_months}-month economic simulation..."):
            results = run_enhanced_parameter_simulation(params, simulation_days, scenario_type)
        
        # Store results for export
        st.session_state.parameter_test_results = {
            'input_parameters': params,
            'simulation_settings': {
                'simulation_months': simulation_months,
                'simulation_days': simulation_days,
                'scenario_type': scenario_type
            },
            'simulation_results': results
        }
        
        # Display results
        display_enhanced_simulation_results(results, params, simulation_months)
    
    # Export functionality
    if export_results and 'parameter_test_results' in st.session_state:
        results_data = st.session_state.parameter_test_results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Calculate summary statistics
        final_result = results_data['simulation_results'][-1] if results_data['simulation_results'] else {}
        initial_result = results_data['simulation_results'][0] if results_data['simulation_results'] else {}
        
        export_content = f"""VCOIN ENHANCED ECONOMIC PARAMETER TESTING REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== INPUT PARAMETERS ===
Platform Metrics:
- Daily Active Users: {results_data['input_parameters']['daily_users']:,}
- Daily Revenue: ${results_data['input_parameters']['daily_revenue']:,}
- User Acquisition Cost: ${results_data['input_parameters']['user_acquisition_cost']:.2f}
- Monthly Acquisition Rate: {results_data['input_parameters']['monthly_acquisition_rate']:.1%}
- Monthly Churn Rate: {results_data['input_parameters']['monthly_churn_rate']:.1%}
- Average Session Duration: {results_data['input_parameters']['avg_session_minutes']:.0f} minutes

Reward Distribution:
- Creator Share: {results_data['input_parameters']['creator_share']:.1%}
- Engagement Share: {results_data['input_parameters']['engagement_share']:.1%}
- Commission Share: {results_data['input_parameters']['commission_share']:.1%}
- Royalty Share: {results_data['input_parameters']['royalty_share']:.1%}

Economic Controls:
- Transaction Fee: {results_data['input_parameters']['transaction_fee_percent']:.1%}
- Staking APY: {results_data['input_parameters']['staking_apy']:.1%}
- Commission Burn Rate: {results_data['input_parameters']['commission_burn_rate']:.1%}
- Annual Inflation Rate: {results_data['input_parameters']['annual_inflation_rate']:.1%}

User Behavior:
- Content Creation Rate: {results_data['input_parameters']['content_creation_rate']:.1%}
- Token Velocity: {results_data['input_parameters']['token_velocity']:.1f}x annually

Token Supply & Pricing:
- Starting Token Price: ${results_data['input_parameters']['initial_price']:.7f}
- Initial Supply: {results_data['input_parameters']['initial_supply']:,} VCOIN
- Max Supply: {results_data['input_parameters']['max_supply']:,} VCOIN

Simulation Settings:
- Simulation Period: {results_data['simulation_settings']['simulation_months']} months ({results_data['simulation_settings']['simulation_days']} days)
- Growth Scenario: {results_data['simulation_settings']['scenario_type']}

=== SIMULATION RESULTS ===
Final Month Metrics:
- Token Supply: {final_result.get('current_supply', 0):,.0f} VCOIN
- Token Price: ${final_result.get('token_price', 0):.7f}
- Market Cap: ${final_result.get('market_cap', 0):,.0f}
- Daily Active Users: {final_result.get('daily_users', 0):,}
- Daily Rewards Distributed: {final_result.get('total_rewards', 0):,.0f} VCOIN
- Daily Tokens Burned: {final_result.get('total_burned', 0):,.0f} VCOIN
- Economic Health Score: {final_result.get('health_score', 0):.1f}/100

Creator Economics:
- Daily Creator Rewards: {final_result.get('creator_rewards', 0):,.0f} VCOIN
- Average Creator Earnings: ${final_result.get('avg_creator_earnings', 0):,.2f}/day
- Total Creator Pool Value: ${final_result.get('creator_pool_value', 0):,.0f}

User Economics:
- Daily Engagement Rewards: {final_result.get('engagement_rewards', 0):,.0f} VCOIN
- Average User Earnings: ${final_result.get('avg_user_earnings', 0):.2f}/day
- User Retention Rate: {final_result.get('user_retention_rate', 0):.1%}

Platform Economics:
- Daily Commission: {final_result.get('commission_rewards', 0):,.0f} VCOIN
- Daily Transaction Fees: ${final_result.get('transaction_fees', 0):,.0f}
- Platform Revenue: ${final_result.get('platform_revenue', 0):,.0f}/day
- User Acquisition ROI: {final_result.get('acquisition_roi', 0):.1f}x

Token Economics:
- Current Inflation Rate: {final_result.get('current_inflation_rate', 0):.2%}
- Actual Token Velocity: {final_result.get('actual_token_velocity', 0):.1f}
- Daily Burn Rate: {final_result.get('daily_burn_rate', 0):.2%}
- Staked Token Percentage: {final_result.get('staked_percentage', 0):.1%}

=== ECONOMIC ANALYSIS ===
Sustainability Metrics:
- Revenue/Cost Ratio: {final_result.get('revenue_cost_ratio', 0):.2f}
- Token Price Stability: {final_result.get('price_stability', 0):.1f}%
- Platform Profitability: {final_result.get('profitability', 'Unknown')}

Growth Trajectory:
- Monthly User Growth: {final_result.get('monthly_user_growth', 0):.1%}
- Monthly Revenue Growth: {final_result.get('monthly_revenue_growth', 0):.1%}
- Token Supply Growth: {final_result.get('supply_growth_rate', 0):.2%}

Risk Assessment:
- Inflation Risk: {final_result.get('inflation_risk', 'Low')}
- User Churn Risk: {final_result.get('churn_risk', 'Medium')}
- Economic Sustainability: {final_result.get('sustainability_risk', 'Good')}

Key Performance Indicators:
- Platform Health Score: {final_result.get('platform_health', 0):.1f}/100
- Token Economy Score: {final_result.get('token_economy_score', 0):.1f}/100
- User Satisfaction Index: {final_result.get('user_satisfaction', 0):.1f}/100

=== COMPREHENSIVE TOKENOMICS ANALYSIS ===

🪙 TOKEN SUPPLY & FLOW ANALYSIS:
- Total Minted During Period: {final_result.get('cumulative_minted', 0):,.0f} VCOIN
- Total Burned During Period: {final_result.get('cumulative_burned', 0):,.0f} VCOIN
- Net Token Flow: {final_result.get('cumulative_minted', 0) - final_result.get('cumulative_burned', 0):,.0f} VCOIN ({('Inflationary' if (final_result.get('cumulative_minted', 0) - final_result.get('cumulative_burned', 0)) > 0 else 'Deflationary')})
- Starting Token Supply: {initial_result.get('current_supply', 0):,.0f} VCOIN
- Final Token Supply: {final_result.get('current_supply', 0):,.0f} VCOIN
- Supply Change: {((final_result.get('current_supply', 1) / initial_result.get('current_supply', 1)) - 1) * 100:+.1f}%

🔄 TOKEN CIRCULATION BREAKDOWN:
- Staked Tokens: {final_result.get('staked_tokens', 0):,.0f} VCOIN ({final_result.get('staked_percentage', 0):.1f}% of total supply)
- Available for Content & NFT: {final_result.get('circulating_for_content', 0):,.0f} VCOIN
- Available for Trading: {final_result.get('circulating_for_trade', 0):,.0f} VCOIN  
- NFT & Content Economy Pool: {final_result.get('circulating_for_nft', 0):,.0f} VCOIN

💎 TOKEN VALUE ANALYSIS:
- Starting Token Price: ${final_result.get('starting_token_value', 0):.7f}
- Ending Token Price: ${final_result.get('ending_token_value', 0):.7f}
- Total Value Change: {final_result.get('total_value_change', 0):+.1f}%
- Starting Market Cap: ${initial_result.get('market_cap', 0):,.0f}
- Final Market Cap: ${final_result.get('market_cap', 0):,.0f}
- Market Cap Change: {((final_result.get('market_cap', 1) / initial_result.get('market_cap', 1)) - 1) * 100:+.1f}%

👥 USER GROWTH ANALYSIS (NET OF CHURN):
- Starting Daily Users: {initial_result.get('daily_users', 0):,.0f}
- Final Daily Users: {final_result.get('daily_users', 0):,.0f}
- Net User Change: {final_result.get('daily_users', 0) - initial_result.get('daily_users', 0):+,.0f}
- User Retention Rate: {final_result.get('user_retention_rate', 0):.1f}%
- Average Monthly Net Growth: {final_result.get('net_monthly_growth', 0):,.0f} users (after churn)
- Monthly Churn Rate: {final_result.get('monthly_churn_rate', 0)*100:.1f}%

🏥 PLATFORM HEALTH & ECONOMY SCORES:
- Platform Health Score: {final_result.get('platform_health', 0):.1f}/100
- Token Economy Score: {final_result.get('token_economy_score', 0):.1f}/100
- User Satisfaction Score: {final_result.get('user_satisfaction', 0):.1f}/100
- Overall Economy Health: {(final_result.get('platform_health', 0) + final_result.get('token_economy_score', 0) + final_result.get('user_satisfaction', 0)) / 3:.1f}/100

💰 DAILY REWARDS ANALYSIS (Content Calculator Aligned):
- Per Content Reward: {final_result.get('enhanced_reward_per_content', 0):,.0f} VCOIN (${final_result.get('enhanced_reward_per_content', 0) * final_result.get('token_price', 0):,.2f})
- Daily Content Pieces: {final_result.get('daily_content_pieces', 0):,.0f} pieces
- Content Multiplier: {final_result.get('total_multiplier', 1.0):.2f}× (Quality + Engagement boost)
- Daily Reward Pool: {final_result.get('total_rewards', 0):,.0f} VCOIN (${final_result.get('total_rewards', 0) * final_result.get('token_price', 0):,.2f})
- Reward Pool Source: {'90% of revenue' if final_result.get('platform_revenue', 0) > 0 else 'Token minting (bootstrap mode)'}
- Average Creator Daily Earnings: ${final_result.get('avg_creator_earnings', 0):.2f} ({final_result.get('avg_creator_earnings', 0) / final_result.get('token_price', 0.01):,.0f} VCOIN)
- Average User Daily Earnings: ${final_result.get('avg_user_earnings', 0):.4f} ({final_result.get('avg_user_earnings', 0) / final_result.get('token_price', 0.01):.2f} VCOIN)
- Daily Platform Revenue: ${final_result.get('platform_revenue', 0):,.0f}

⚖️ ECONOMY WORKING INDICATORS:
Economy Health Score: {((25 if abs(final_result.get('total_value_change', 0)) < 20 else 15 if abs(final_result.get('total_value_change', 0)) < 50 else 0) + (25 if final_result.get('daily_users', 0) > initial_result.get('daily_users', 0) else 0) + (25 if 0.7 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.3 else 15 if 0.5 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.5 else 0) + (25 if final_result.get('revenue_cost_ratio', 0) > 1.2 else 15 if final_result.get('revenue_cost_ratio', 0) > 1.0 else 0))}/100

Economic Status: {('🎉 ECONOMY IS WORKING!' if ((25 if abs(final_result.get('total_value_change', 0)) < 20 else 15 if abs(final_result.get('total_value_change', 0)) < 50 else 0) + (25 if final_result.get('daily_users', 0) > initial_result.get('daily_users', 0) else 0) + (25 if 0.7 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.3 else 15 if 0.5 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.5 else 0) + (25 if final_result.get('revenue_cost_ratio', 0) > 1.2 else 15 if final_result.get('revenue_cost_ratio', 0) > 1.0 else 0)) >= 80 else '⚠️ ECONOMY IS STABLE' if ((25 if abs(final_result.get('total_value_change', 0)) < 20 else 15 if abs(final_result.get('total_value_change', 0)) < 50 else 0) + (25 if final_result.get('daily_users', 0) > initial_result.get('daily_users', 0) else 0) + (25 if 0.7 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.3 else 15 if 0.5 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.5 else 0) + (25 if final_result.get('revenue_cost_ratio', 0) > 1.2 else 15 if final_result.get('revenue_cost_ratio', 0) > 1.0 else 0)) >= 60 else '❌ ECONOMY NEEDS WORK')}

Key Health Indicators:
- Token Price Stability: {'✅ Stable (< 20% change)' if abs(final_result.get('total_value_change', 0)) < 20 else '⚠️ Moderately Volatile (20-50% change)' if abs(final_result.get('total_value_change', 0)) < 50 else '❌ Highly Volatile (> 50% change)'}
- User Growth vs Churn: {'✅ User base growing despite churn' if final_result.get('daily_users', 0) > initial_result.get('daily_users', 0) else '❌ User base declining due to churn'}
- Token Supply Balance: {'✅ Healthy burn/mint ratio (0.7-1.3)' if 0.7 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.3 else '⚠️ Moderate burn/mint ratio (0.5-1.5)' if 0.5 <= (final_result.get('cumulative_burned', 1) / max(1, final_result.get('cumulative_minted', 1))) <= 1.5 else '❌ Unhealthy burn/mint ratio'}
- Platform Sustainability: {'✅ Platform profitable (revenue > costs)' if final_result.get('revenue_cost_ratio', 0) > 1.2 else '⚠️ Platform break-even' if final_result.get('revenue_cost_ratio', 0) > 1.0 else '❌ Platform losing money'}

Burn/Mint Ratio: {final_result.get('cumulative_burned', 0) / max(1, final_result.get('cumulative_minted', 1)):.2f}
Revenue/Cost Ratio: {final_result.get('revenue_cost_ratio', 0):.2f}
Price Volatility: {abs(final_result.get('total_value_change', 0)):.1f}%
"""
        
        st.download_button(
            label="📄 Download Parameter Test Report",
            data=export_content,
            file_name=f"vcoin_parameter_test_{timestamp}.txt",
            mime="text/plain",
            width="stretch"
        )

def run_parameter_simulation(params: Dict[str, Any], days: int, scenario: str) -> List[Dict[str, Any]]:
    """Run economic simulation with given parameters"""
    
    # Initialize economic engine
    engine = VCoinEconomicEngine(params)
    
    # Define scenario parameters
    scenario_configs = {
        "Conservative": {
            'max_users': params['daily_users'] * 5,
            'growth_rate': 0.005,
            'base_daily_revenue': params['daily_revenue'],
            'content_creation_rate': 0.03
        },
        "Moderate": {
            'max_users': params['daily_users'] * 10,
            'growth_rate': 0.008,
            'base_daily_revenue': params['daily_revenue'],
            'content_creation_rate': 0.05
        },
        "Aggressive": {
            'max_users': params['daily_users'] * 20,
            'growth_rate': 0.015,
            'base_daily_revenue': params['daily_revenue'],
            'content_creation_rate': 0.08
        }
    }
    
    scenario_params = scenario_configs[scenario]
    
    # Run simulation
    results = engine.run_simulation(scenario_params, days)
    
    return results

def display_simulation_results(results: List[Dict[str, Any]], params: Dict[str, Any]):
    """Display simulation results with charts and metrics"""
    
    if not results:
        st.error("No simulation results to display")
        return
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)
    
    # Key metrics display
    st.subheader("📊 Simulation Results")
    
    # Top-level metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        final_price = df['current_price'].iloc[-1]
        initial_price = df['current_price'].iloc[0]
        price_change = (final_price / initial_price) - 1
        st.metric(
            "Final Token Price", 
            f"${final_price:.7f}",
            f"{price_change:.1%}"
        )
    
    with col2:
        final_supply = df['total_supply'].iloc[-1]
        initial_supply = df['total_supply'].iloc[0]
        supply_change = (final_supply / initial_supply) - 1
        st.metric(
            "Total Supply", 
            f"{final_supply:,.0f}",
            f"{supply_change:.1%}"
        )
    
    with col3:
        avg_daily_rewards = df['daily_rewards'].mean()
        st.metric("Avg Daily Rewards", f"{avg_daily_rewards:,.0f} VCOIN")
    
    with col4:
        avg_daily_burns = df['daily_burns'].mean()
        st.metric("Avg Daily Burns", f"{avg_daily_burns:,.0f} VCOIN")
    
    # Economic health indicators
    st.subheader("🏥 Economic Health")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        avg_inflation = df['inflation_rate'].mean()
        inflation_color = "normal" if -0.05 <= avg_inflation <= 0.15 else "inverse"
        st.metric("Avg Inflation Rate", f"{avg_inflation:.1%}", delta_color=inflation_color)
    
    with col6:
        avg_velocity = df['token_velocity'].mean()
        velocity_color = "normal" if 1.5 <= avg_velocity <= 3.0 else "inverse"
        st.metric("Token Velocity", f"{avg_velocity:.2f}", delta_color=velocity_color)
    
    with col7:
        total_creator_rewards = df['daily_rewards'].sum() * params['creator_share']
        avg_creator_daily = total_creator_rewards / len(df) / (df['content_count'].mean() / df['active_users'].mean() * 0.05)
        st.metric("Avg Creator Daily Earnings", f"{avg_creator_daily:.0f} VCOIN")
    
    with col8:
        burn_efficiency = df['daily_burns'].sum() / df['daily_rewards'].sum()
        efficiency_color = "normal" if burn_efficiency > 0.3 else "inverse"
        st.metric("Burn Efficiency", f"{burn_efficiency:.1%}", delta_color=efficiency_color)
    
    # Charts
    create_economic_charts(df)
    
    # Detailed breakdown
    with st.expander("📋 Detailed Economic Breakdown"):
        display_detailed_breakdown(df, params)
    
    # Export functionality
    if st.button("💾 Export Simulation Data"):
        export_simulation_data(df, params)

def create_economic_charts(df: pd.DataFrame):
    """Create comprehensive economic visualization charts"""
    
    # Chart 1: Token Price and Supply Over Time
    fig1 = make_subplots(
        rows=2, cols=1,
        subplot_titles=('VCOIN Price Over Time', 'Token Supply Over Time'),
        vertical_spacing=0.1
    )
    
    # Price chart
    fig1.add_trace(
        go.Scatter(
            x=df['day'], 
            y=df['current_price'], 
            name='VCOIN Price ($)', 
            line=dict(color='#1f77b4', width=3)
        ),
        row=1, col=1
    )
    
    # Supply chart
    fig1.add_trace(
        go.Scatter(
            x=df['day'], 
            y=df['total_supply'], 
            name='Total Supply', 
            line=dict(color='#2ca02c', width=3)
        ),
        row=2, col=1
    )
    
    fig1.update_layout(
        height=600, 
        title_text="📈 Token Economics Over Time",
        showlegend=False
    )
    fig1.update_xaxes(title_text="Day", row=2, col=1)
    fig1.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig1.update_yaxes(title_text="Supply (VCOIN)", row=2, col=1)
    
    st.plotly_chart(fig1, width="stretch")
    
    # Chart 2: Daily Token Flows
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=df['day'], 
        y=df['daily_rewards'], 
        name='Daily Rewards', 
        line=dict(color='#ff7f0e', width=2),
        fill='tonexty'
    ))
    
    fig2.add_trace(go.Scatter(
        x=df['day'], 
        y=df['daily_burns'], 
        name='Daily Burns', 
        line=dict(color='#d62728', width=2),
        fill='tozeroy'
    ))
    
    # Add net flow
    df['net_flow'] = df['daily_rewards'] - df['daily_burns']
    fig2.add_trace(go.Scatter(
        x=df['day'],
        y=df['net_flow'],
        name='Net Flow',
        line=dict(color='#9467bd', width=3, dash='dash')
    ))
    
    fig2.update_layout(
        title="🔄 Daily Token Flows: Rewards vs Burns",
        xaxis_title="Day",
        yaxis_title="VCOIN",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig2, width="stretch")
    
    # Chart 3: Economic Health Dashboard
    fig3 = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Inflation Rate (%)', 'Token Velocity', 'User Growth', 'Revenue Growth'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Inflation rate
    fig3.add_trace(
        go.Scatter(x=df['day'], y=df['inflation_rate']*100, name='Inflation %', line=dict(color='red')),
        row=1, col=1
    )
    
    # Token velocity
    fig3.add_trace(
        go.Scatter(x=df['day'], y=df['token_velocity'], name='Velocity', line=dict(color='blue')),
        row=1, col=2
    )
    
    # User growth
    fig3.add_trace(
        go.Scatter(x=df['day'], y=df['active_users'], name='Users', line=dict(color='green')),
        row=2, col=1
    )
    
    # Revenue growth
    fig3.add_trace(
        go.Scatter(x=df['day'], y=df['daily_revenue'], name='Revenue', line=dict(color='orange')),
        row=2, col=2
    )
    
    fig3.update_layout(height=600, title_text="📊 Economic Health Dashboard", showlegend=False)
    st.plotly_chart(fig3, width="stretch")

def price_discovery_interface():
    """Cold start price discovery tool"""
    
    st.header("💰 VCOIN Cold Start Price Discovery")
    st.markdown("Calculate fair initial token price using multiple valuation methods")
    
    # Input form
    with st.form("price_discovery_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Platform Projections")
            expected_dau = st.number_input("Expected Daily Active Users", 1_000, 10_000_000, 100_000)
            expected_revenue = st.number_input("Expected Daily Revenue ($)", 1_000, 1_000_000, 50_000)
            expected_creators = st.number_input("Expected Daily Creators", 100, 100_000, 5_000)
            
        with col2:
            st.subheader("💸 Development Costs")
            dev_cost = st.number_input("Development Cost ($)", 500_000, 10_000_000, 2_000_000)
            annual_operating = st.number_input("Annual Operating Cost ($)", 1_000_000, 20_000_000, 5_000_000)
            marketing_budget = st.number_input("Annual Marketing Budget ($)", 100_000, 10_000_000, 2_000_000)
        
        # Token supply
        st.subheader("🪙 Token Supply")
        col3, col4 = st.columns(2)
        with col3:
            initial_supply = st.number_input("Initial Supply", 500_000_000, 2_000_000_000, 1_000_000_000)
        with col4:
            max_supply = st.number_input("Max Supply", 5_000_000_000, 20_000_000_000, 10_000_000_000)
        
        submitted = st.form_submit_button("💡 Calculate Initial Price", type="primary")
    
    if submitted:
        # Prepare metrics for valuation
        platform_metrics = {
            'daily_active_users': expected_dau,
            'daily_revenue': expected_revenue,
            'daily_creators': expected_creators,
            'initial_supply': initial_supply,
            'max_supply': max_supply,
            'development_cost': dev_cost,
            'annual_operating_cost': annual_operating,
            'marketing_budget': marketing_budget
        }
        
        # Calculate valuation
        valuator = VCoinColdStartValuation()
        valuation_result = valuator.calculate_initial_price(platform_metrics)
        
        # Display results
        st.success("✅ Price Discovery Complete")
        
        # Main recommendation
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🎯 Recommended Price", 
                f"${valuation_result['recommended_price']:.4f}"
            )
        
        with col2:
            low_range = valuation_result['confidence_range'][0]
            st.metric("📉 Conservative Price", f"${low_range:.4f}")
        
        with col3:
            high_range = valuation_result['confidence_range'][1]
            st.metric("📈 Optimistic Price", f"${high_range:.4f}")
        
        # Valuation method breakdown
        st.subheader("🔍 Valuation Method Breakdown")
        
        method_data = []
        for method, price in valuation_result['individual_valuations'].items():
            weight = valuation_result['valuation_weights'][method]
            contribution = price * weight
            
            method_data.append({
                'Method': method.replace('_', ' ').title(),
                'Price': f"${price:.4f}",
                'Weight': f"{weight:.0%}",
                'Contribution': f"${contribution:.4f}",
                'Rationale': get_method_rationale(method)
            })
        
        method_df = pd.DataFrame(method_data)
        st.table(method_df)
        
        # Price sensitivity analysis
        st.subheader("📊 Price Sensitivity Analysis")
        
        sensitivity_data = []
        for factor in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
            adjusted_metrics = platform_metrics.copy()
            adjusted_metrics['daily_revenue'] *= factor
            adjusted_metrics['daily_active_users'] = int(adjusted_metrics['daily_active_users'] * factor)
            
            adjusted_valuation = valuator.calculate_initial_price(adjusted_metrics)
            
            sensitivity_data.append({
                'Revenue Multiple': f"{factor}x",
                'Recommended Price': f"${adjusted_valuation['recommended_price']:.4f}",
                'Price Change': f"{((adjusted_valuation['recommended_price'] / valuation_result['recommended_price']) - 1):.1%}"
            })
        
        sensitivity_df = pd.DataFrame(sensitivity_data)
        st.table(sensitivity_df)

def economy_scale_simulator_interface():
    """Comprehensive economy analysis across different user scales and engagement scenarios"""
    
    st.header("📈 Economy Scale Simulator")
    st.markdown("**Analyze VCOIN economy across different platform sizes and engagement patterns**")
    
    # Platform benchmark selection
    st.subheader("📱 Platform Reference Model")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        platform_model = st.selectbox(
            "Select Platform Benchmark:",
            ['hybrid_ig_x', 'instagram_like', 'x_twitter_like', 'youtube_like', 'custom'],
            format_func=lambda x: {
                'hybrid_ig_x': '🔄 Hybrid (Instagram + X) - Recommended',
                'instagram_like': '📸 Instagram Model (5-10% engagement)',
                'x_twitter_like': '🐦 X/Twitter Model (1-3% engagement)', 
                'youtube_like': '📺 YouTube Model (2-6% engagement)',
                'custom': '⚙️ Custom Engagement Ratios'
            }[x],
            help="💡 Select platform model to determine engagement ratios"
        )
    
    with col2:
        st.info(f"**Selected Model Ratios:**")
    
    # Define platform engagement ratios based on research
    platform_ratios = {
        'hybrid_ig_x': {
            'view_to_like': 0.055,      # Average of IG (7.5%) and X (2.5%) = 5.5%
            'like_to_comment': 0.065,   # Average of IG (5%) and X (8%) = 6.5%
            'like_to_share': 0.225,     # Average of IG (7.5%) and X (35%) = 22.5%
            'base_engagement': 0.045,   # 3-6% range average = 4.5%
            'description': 'Balanced engagement combining visual and text-based interactions'
        },
        'instagram_like': {
            'view_to_like': 0.075,      # 5-10% average = 7.5%
            'like_to_comment': 0.035,   # 2-5% average = 3.5%
            'like_to_share': 0.075,     # 5-10% average = 7.5%
            'base_engagement': 0.055,   # Higher visual engagement
            'description': 'High visual engagement, moderate sharing, lower commenting'
        },
        'x_twitter_like': {
            'view_to_like': 0.015,      # 1-2% average = 1.5%
            'like_to_comment': 0.10,    # ~10%
            'like_to_share': 0.35,      # 30-40% average = 35%
            'base_engagement': 0.025,   # Lower overall but high sharing
            'description': 'Lower engagement but very high sharing/retweet rates'
        },
        'youtube_like': {
            'view_to_like': 0.04,       # 3-5% average = 4%
            'like_to_comment': 0.0075,  # 0.5-1% average = 0.75%
            'view_to_comment': 0.003,   # Direct view to comment
            'base_engagement': 0.04,    # Moderate engagement
            'description': 'Moderate likes, very low comments, minimal sharing'
        },
        'custom': {
            'view_to_like': 0.05,
            'like_to_comment': 0.05,
            'like_to_share': 0.15,
            'base_engagement': 0.04,
            'description': 'Custom ratios - adjust manually'
        }
    }
    
    ratios = platform_ratios[platform_model]
    
    # Display selected ratios
    with col2:
        st.markdown(f"""
        **{platform_model.replace('_', ' ').title()} Ratios:**
        - View → Like: {ratios['view_to_like']:.1%}
        - Like → Comment: {ratios['like_to_comment']:.1%}
        - Like → Share: {ratios['like_to_share']:.1%}
        - Base Engagement: {ratios['base_engagement']:.1%}
        """)
    
    st.info(f"**📊 Platform Logic:** {ratios['description']}")
    
    # Content-driven model explanation
    with st.expander("💡 Content-Driven Tokenomics Explanation", expanded=False):
        st.markdown("""
        **🎯 Content-Driven Minting Model:**
        
        **Traditional Model Problems:**
        - Fixed daily minting regardless of activity
        - No connection between content creation and token supply
        - Inflation without value creation
        - Poor scaling with platform growth
        
        **Content-Driven Model Benefits:**
        - **Minting tied to content**: Only mint when content is created
        - **Quality-based minting**: Better content = more tokens minted
        - **NFT premium minting**: NFT-eligible content gets bonus minting
        - **Natural scaling**: More content = more tokens, automatically
        - **No empty inflation**: No minting without value creation
        
        **Burn Mechanisms:**
        - **Commission burns**: Platform fees get burned for deflation
        - **Quality penalties**: Low-engagement content triggers burns
        - **NFT trading burns**: Trading fees get burned
        - **Promotion burns**: Creators pay tokens for visibility
        - **Spam penalties**: Excessive posting gets penalized
        
        **Result**: Self-balancing economy that scales organically with content creation!
        """)
    
    # Economic parameters
    st.subheader("💰 Economic Parameters")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        revenue_mode = st.radio(
            "Revenue Model:",
            ['bootstrap_mode', 'revenue_backed'],
            format_func=lambda x: {
                'bootstrap_mode': '🚀 Bootstrap Mode (Token Minting)',
                'revenue_backed': '💰 Revenue-Backed Mode'
            }[x]
        )
        
        if revenue_mode == 'revenue_backed':
            revenue_per_1k_users = st.number_input(
                "Revenue per 1K Users/Day ($)",
                min_value=1, max_value=10000, value=500, step=50,
                help="💡 Daily revenue generated per 1,000 active users"
            )
        else:
            # Content-driven minting approach
            st.markdown("**🎯 Content-Driven Token Minting:**")
            
            tokens_per_content = st.number_input(
                "VCOIN Minted per Content Piece",
                min_value=100, max_value=10000, value=1000, step=100,
                help="💡 Fixed VCOIN amount minted for each piece of content created (scales with content volume)"
            )
            
            nft_mint_multiplier = st.slider(
                "NFT Content Mint Multiplier",
                min_value=1.0, max_value=5.0, value=2.0, step=0.1,
                help="💡 Extra minting multiplier for NFT-eligible content (2.0 = double minting)"
            )
            
            nft_content_percentage = st.slider(
                "NFT-Eligible Content (%)",
                min_value=5, max_value=50, value=15, step=5,
                help="💡 Percentage of content that becomes NFTs and gets extra minting"
            )
    
    with col2:
        vcoin_price = st.number_input(
            "VCOIN Token Price ($)",
            min_value=0.0000001, max_value=10.0, value=0.10, step=0.01, format="%.7f",
            help="💡 Current VCOIN token price for calculations"
        )
        
        total_supply = st.number_input(
            "Total Token Supply",
            min_value=1_000_000, max_value=50_000_000_000, value=1_000_000_000, step=1_000_000,
            help="💡 Total VCOIN supply"
        )
    
    with col3:
        creator_percentage = st.slider(
            "Creator Percentage (%)",
            min_value=1, max_value=10, value=3, step=1,
            help="💡 % of users who create content daily"
        )
        
        posts_per_creator = st.slider(
            "Posts per Creator/Day",
            min_value=1, max_value=10, value=2, step=1,
            help="💡 Average content pieces per creator daily"
        )
    
    # Enhanced burn mechanisms
    st.subheader("🔥 Content-Driven Burn Mechanisms")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        commission_burn_rate = st.slider(
            "Commission Burn Rate (%)",
            min_value=10, max_value=50, value=25, step=5,
            help="💡 % of platform commission that gets burned (deflationary pressure)"
        )
        
        quality_penalty_burn = st.slider(
            "Quality Penalty Burn (%)",
            min_value=0, max_value=30, value=10, step=5,
            help="💡 % of rewards burned for low-engagement content (< 1% engagement)"
        )
    
    with col2:
        nft_trading_burn = st.slider(
            "NFT Trading Burn (%)",
            min_value=1, max_value=10, value=3, step=1,
            help="💡 % of NFT trading volume that gets burned"
        )
        
        engagement_reward_burn = st.slider(
            "Engagement Reward Burn (%)",
            min_value=0, max_value=15, value=5, step=1,
            help="💡 % of engagement rewards that get burned (circulation control)"
        )
    
    with col3:
        promotion_burn_rate = st.slider(
            "Content Promotion Burn Rate",
            min_value=0.0, max_value=2.0, value=0.5, step=0.1,
            help="💡 VCOIN burned per view for content promotion (creators pay for visibility)"
        )
        
        spam_penalty_multiplier = st.slider(
            "Spam Penalty Multiplier",
            min_value=1.0, max_value=5.0, value=2.0, step=0.5,
            help="💡 Burn multiplier for excessive posting (anti-spam mechanism)"
        )
    
    # Growth phases configuration
    st.subheader("🚀 Growth Phase Analysis")
    
    # Define the four phases with user counts
    phases = [
        {'name': 'Phase 1: Early Adoption', 'users': 1_000, 'emoji': '🌱'},
        {'name': 'Phase 2: Growth', 'users': 10_000, 'emoji': '📈'},
        {'name': 'Phase 3: Scale', 'users': 100_000, 'emoji': '🚀'},
        {'name': 'Phase 4: Mass Market', 'users': 1_000_000, 'emoji': '🌍'}
    ]
    
    if st.button("🧮 Analyze Economy Across All Phases", type="primary"):
        
        results = []
        
        for phase in phases:
            phase_users = phase['users']
            phase_creators = int(phase_users * (creator_percentage / 100))
            phase_daily_content = phase_creators * posts_per_creator
            
            # Calculate content distribution (popular/normal/low engagement)
            popular_content = int(phase_daily_content * 0.10)  # 10% popular
            normal_content = int(phase_daily_content * 0.70)   # 70% normal  
            low_content = int(phase_daily_content * 0.20)      # 20% low
            
            # Calculate engagement metrics for each content type based on phase
            content_scenarios = []
            
            # Popular content engagement
            if phase_users <= 1_000:
                popular_views = 550  # 500-600 average
                popular_likes = int(popular_views * ratios['view_to_like'] * 1.8)  # 80% boost for popular
                popular_comments = int(popular_likes * ratios['like_to_comment'])
                popular_shares = int(popular_likes * ratios['like_to_share'])
            elif phase_users <= 10_000:
                popular_views = 5_000  # 4K-6K average
                popular_likes = int(popular_views * ratios['view_to_like'] * 1.8)
                popular_comments = int(popular_likes * ratios['like_to_comment'])
                popular_shares = int(popular_likes * ratios['like_to_share'])
            elif phase_users <= 100_000:
                popular_views = 50_000  # 40K-60K average
                popular_likes = int(popular_views * ratios['view_to_like'] * 1.8)
                popular_comments = int(popular_likes * ratios['like_to_comment'])
                popular_shares = int(popular_likes * ratios['like_to_share'])
            else:  # 1M users
                popular_views = 500_000  # 400K-600K average
                popular_likes = int(popular_views * ratios['view_to_like'] * 1.8)
                popular_comments = int(popular_likes * ratios['like_to_comment'])
                popular_shares = int(popular_likes * ratios['like_to_share'])
            
            # Normal content engagement
            normal_views = int(popular_views * 0.35)  # 35% of popular views
            normal_likes = int(normal_views * ratios['view_to_like'])
            normal_comments = int(normal_likes * ratios['like_to_comment'])
            normal_shares = int(normal_likes * ratios['like_to_share'])
            
            # Low engagement content
            low_views = int(popular_views * 0.15)  # 15% of popular views
            low_likes = int(low_views * ratios['view_to_like'] * 0.6)  # 40% lower engagement
            low_comments = int(low_likes * ratios['like_to_comment'])
            low_shares = int(low_likes * ratios['like_to_share'])
            
            content_scenarios = [
                {'type': 'popular', 'count': popular_content, 'views': popular_views, 'likes': popular_likes, 'comments': popular_comments, 'shares': popular_shares},
                {'type': 'normal', 'count': normal_content, 'views': normal_views, 'likes': normal_likes, 'comments': normal_comments, 'shares': normal_shares},
                {'type': 'low', 'count': low_content, 'views': low_views, 'likes': low_likes, 'comments': low_comments, 'shares': low_shares}
            ]
            
            # Calculate total daily metrics for this phase
            total_daily_views = sum(scenario['count'] * scenario['views'] for scenario in content_scenarios)
            total_daily_likes = sum(scenario['count'] * scenario['likes'] for scenario in content_scenarios)
            total_daily_comments = sum(scenario['count'] * scenario['comments'] for scenario in content_scenarios)
            total_daily_shares = sum(scenario['count'] * scenario['shares'] for scenario in content_scenarios)
            
            # Calculate content-driven minting for this phase
            if revenue_mode == 'revenue_backed':
                phase_daily_revenue = (phase_users / 1000) * revenue_per_1k_users
                reward_pool_usd = phase_daily_revenue * 0.90  # 90% to rewards
                reward_pool_tokens = reward_pool_usd / vcoin_price
                tokens_minted_for_content = 0  # No additional minting in revenue mode
            else:
                # Content-driven minting: mint tokens based on content creation
                regular_content = int(phase_daily_content * (100 - nft_content_percentage) / 100)
                nft_content = int(phase_daily_content * nft_content_percentage / 100)
                
                # Calculate minting based on content
                regular_minting = regular_content * tokens_per_content
                nft_minting = nft_content * tokens_per_content * nft_mint_multiplier
                
                # Quality-based minting adjustments
                total_engagement_rate = (total_daily_likes + total_daily_comments + total_daily_shares) / max(1, total_daily_views)
                
                if total_engagement_rate > 0.05:  # High engagement (>5%)
                    quality_bonus = 1.5
                elif total_engagement_rate > 0.02:  # Medium engagement (2-5%)
                    quality_bonus = 1.0
                else:  # Low engagement (<2%)
                    quality_bonus = 0.75
                
                # Total content-driven minting
                tokens_minted_for_content = (regular_minting + nft_minting) * quality_bonus
                reward_pool_tokens = tokens_minted_for_content
                reward_pool_usd = reward_pool_tokens * vcoin_price
            
            # Calculate per-content rewards (matching Content Calculator logic)
            base_reward_per_content = reward_pool_tokens / max(1, phase_daily_content)
            
            # Apply average multipliers
            avg_multiplier = 1.2 * 1.5 * 1.3  # Content × Engagement × Quality = 2.34×
            enhanced_reward_per_content = base_reward_per_content * avg_multiplier
            
            # Calculate total rewards and burns
            total_daily_content_rewards = enhanced_reward_per_content * phase_daily_content
            
            # Content-driven burn mechanisms
            platform_commission = total_daily_content_rewards * 0.10
            commission_burn = platform_commission * (commission_burn_rate / 100)
            
            # Quality-based burns
            low_engagement_content = sum(1 for scenario in content_scenarios 
                                       if (scenario['likes'] + scenario['comments'] + scenario['shares']) / max(1, scenario['views']) < 0.01)
            quality_penalty_total = low_engagement_content * enhanced_reward_per_content * (quality_penalty_burn / 100)
            
            # Activity-based burns
            nft_volume = nft_content * enhanced_reward_per_content * 0.3  # Assume 30% of NFT rewards get traded
            nft_burn = nft_volume * (nft_trading_burn / 100)
            
            # Promotion burns (creators pay for visibility)
            promotion_burn = total_daily_views * promotion_burn_rate
            
            # Engagement reward burns
            total_engagement_rewards = total_daily_content_rewards * 0.50  # 50% goes to engagement
            engagement_burn = total_engagement_rewards * (engagement_reward_burn / 100)
            
            # Spam penalty burns (for excessive posting)
            avg_posts_per_creator = phase_daily_content / max(1, phase_creators)
            if avg_posts_per_creator > 5:  # Excessive posting threshold
                spam_penalty = (avg_posts_per_creator - 5) * phase_creators * 100 * spam_penalty_multiplier
            else:
                spam_penalty = 0
            
            total_daily_burns = commission_burn + quality_penalty_total + nft_burn + promotion_burn + engagement_burn + spam_penalty
            
            # Net token flow
            net_daily_flow = reward_pool_tokens - total_daily_burns
            
            # Store phase results with enhanced content-driven metrics
            phase_result = {
                'phase_name': phase['name'],
                'emoji': phase['emoji'],
                'users': phase_users,
                'creators': phase_creators,
                'daily_content': phase_daily_content,
                'regular_content': regular_content if revenue_mode == 'bootstrap_mode' else phase_daily_content,
                'nft_content': nft_content if revenue_mode == 'bootstrap_mode' else 0,
                'content_scenarios': content_scenarios,
                'total_views': total_daily_views,
                'total_likes': total_daily_likes,
                'total_comments': total_daily_comments,
                'total_shares': total_daily_shares,
                'engagement_rate': (total_daily_likes + total_daily_comments + total_daily_shares) / max(1, total_daily_views),
                'quality_bonus': quality_bonus if revenue_mode == 'bootstrap_mode' else 1.0,
                'daily_revenue': phase_daily_revenue if revenue_mode == 'revenue_backed' else 0,
                'reward_pool_tokens': reward_pool_tokens,
                'reward_pool_usd': reward_pool_usd,
                'base_reward_per_content': base_reward_per_content,
                'enhanced_reward_per_content': enhanced_reward_per_content,
                'total_content_rewards': total_daily_content_rewards,
                'total_burns': total_daily_burns,
                'commission_burn': commission_burn,
                'quality_penalty_burn': quality_penalty_total,
                'nft_trading_burn': nft_burn,
                'promotion_burn': promotion_burn,
                'engagement_burn': engagement_burn,
                'spam_penalty_burn': spam_penalty,
                'net_token_flow': net_daily_flow,
                'tokens_minted': tokens_minted_for_content if revenue_mode == 'bootstrap_mode' else 0,
                'tokens_burned': total_daily_burns,
                'burn_mint_ratio': total_daily_burns / max(1, tokens_minted_for_content) if revenue_mode == 'bootstrap_mode' else 0,
                'minting_efficiency': tokens_minted_for_content / max(1, phase_daily_content) if revenue_mode == 'bootstrap_mode' else 0,
                'economy_health': min(100, 
                    (enhanced_reward_per_content / 1000) * 25 +  # Reward adequacy
                    (min(1, total_daily_burns / max(1, tokens_minted_for_content)) * 50) +  # Burn balance
                    (min(1, total_engagement_rate * 20) * 25)  # Engagement health
                ) if revenue_mode == 'bootstrap_mode' else min(100, (enhanced_reward_per_content / 100) * 30 + (phase_users / 10000) * 40 + 30)
            }
            
            results.append(phase_result)
        
        # Display comprehensive results
        st.success("✅ Economy Scale Analysis Complete")
        
        # Phase comparison overview
        st.subheader("🏆 Economy Scale Comparison")
        
        # Create enhanced comparison table
        comparison_data = {
            'Phase': [r['emoji'] + ' ' + r['phase_name'] for r in results],
            'Users': [f"{r['users']:,}" for r in results],
            'Content/Day': [f"{r['daily_content']:,}" for r in results],
            'Minted/Content': [f"{r['minting_efficiency']:,.0f} VCOIN" if r['minting_efficiency'] > 0 else "Revenue-backed" for r in results],
            'Total Minted': [f"{r['tokens_minted']:,.0f} VCOIN" for r in results],
            'Total Burned': [f"{r['tokens_burned']:,.0f} VCOIN" for r in results],
            'Burn/Mint Ratio': [f"{r['burn_mint_ratio']:.2f}" if r['burn_mint_ratio'] > 0 else "N/A" for r in results],
            'Net Flow': [f"{r['net_token_flow']:+,.0f}" for r in results],
            'Health': [f"{r['economy_health']:.0f}/100" for r in results]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)
        
        # Detailed phase analysis
        st.subheader("📊 Detailed Phase Analysis")
        
        for i, result in enumerate(results):
            with st.expander(f"{result['emoji']} {result['phase_name']} - {result['users']:,} Users", expanded=i==0):
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    st.markdown("**👥 User Metrics:**")
                    st.write(f"• Active Users: {result['users']:,}")
                    st.write(f"• Daily Creators: {result['creators']:,} ({creator_percentage}%)")
                    st.write(f"• Daily Content: {result['daily_content']:,} pieces")
                    st.write(f"• Posts per Creator: {posts_per_creator}")
                    
                    st.markdown("**📈 Engagement Totals:**")
                    st.write(f"• Total Views: {result['total_views']:,}")
                    st.write(f"• Total Likes: {result['total_likes']:,}")
                    st.write(f"• Total Comments: {result['total_comments']:,}")
                    st.write(f"• Total Shares: {result['total_shares']:,}")
                    st.write(f"• Overall Engagement: {result['engagement_rate']:.1%}")
                
                with col2:
                    st.markdown("**🪙 Content-Driven Token Economics:**")
                    if revenue_mode == 'bootstrap_mode':
                        st.write(f"• Regular Content: {result['regular_content']:,} pieces")
                        st.write(f"• NFT Content: {result['nft_content']:,} pieces ({nft_content_percentage}%)")
                        st.write(f"• Quality Bonus: {result['quality_bonus']:.2f}× (engagement-based)")
                        st.write(f"• Minting per Content: {result['minting_efficiency']:,.0f} VCOIN")
                    else:
                        st.write(f"• Revenue Pool: ${result['reward_pool_usd']:,.0f}")
                        st.write(f"• Token Pool: {result['reward_pool_tokens']:,.0f} VCOIN")
                    
                    st.write(f"• Enhanced per Content: {result['enhanced_reward_per_content']:,.0f} VCOIN")
                    st.write(f"• Total Content Rewards: {result['total_content_rewards']:,.0f} VCOIN")
                    
                    st.markdown("**🔥 Content-Driven Token Flow:**")
                    st.write(f"• Daily Minted: {result['tokens_minted']:,.0f} VCOIN")
                    st.write(f"• Daily Burned: {result['tokens_burned']:,.0f} VCOIN")
                    if result['burn_mint_ratio'] > 0:
                        st.write(f"• Burn/Mint Ratio: {result['burn_mint_ratio']:.2f}")
                    flow_status = "Inflationary" if result['net_token_flow'] > 0 else "Deflationary"
                    st.write(f"• Net Flow: {result['net_token_flow']:+,.0f} VCOIN ({flow_status})")
                
                with col3:
                    st.markdown("**🎯 Content Breakdown:**")
                    for scenario in result['content_scenarios']:
                        st.write(f"**{scenario['type'].title()} ({scenario['count']} pieces):**")
                        st.write(f"  - {scenario['views']:,} views")
                        st.write(f"  - {scenario['likes']:,} likes")
                        st.write(f"  - {scenario['comments']:,} comments") 
                        st.write(f"  - {scenario['shares']:,} shares")
                    
                    st.markdown("**🔥 Burn Breakdown:**")
                    st.write(f"• Commission Burn: {result['commission_burn']:,.0f} VCOIN")
                    st.write(f"• Quality Penalty: {result['quality_penalty_burn']:,.0f} VCOIN")
                    st.write(f"• NFT Trading: {result['nft_trading_burn']:,.0f} VCOIN")
                    st.write(f"• Promotion: {result['promotion_burn']:,.0f} VCOIN")
                    st.write(f"• Engagement: {result['engagement_burn']:,.0f} VCOIN")
                    st.write(f"• Spam Penalty: {result['spam_penalty_burn']:,.0f} VCOIN")
                    
                    st.markdown("**💡 Economy Health:**")
                    health_score = result['economy_health']
                    if health_score >= 80:
                        st.success(f"🎉 Excellent: {health_score:.0f}/100")
                    elif health_score >= 60:
                        st.warning(f"⚠️ Good: {health_score:.0f}/100")
                    else:
                        st.error(f"❌ Needs Work: {health_score:.0f}/100")
        
        # VCOIN Generation Summary
        st.markdown("---")
        st.subheader("💎 VCOIN Generation Summary")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🪙 Daily VCOIN Generation by Phase:**")
            for result in results:
                multiplier = result['users'] / 1000  # Show as multiple of 1K users
                st.write(f"• **{result['emoji']} {multiplier:,.0f}K Users**: {result['tokens_minted']:,.0f} VCOIN minted")
        
        with col2:
            st.markdown("**🔥 Daily VCOIN Burning by Phase:**")
            for result in results:
                multiplier = result['users'] / 1000
                burn_rate = (result['tokens_burned'] / result['tokens_minted']) * 100 if result['tokens_minted'] > 0 else 0
                st.write(f"• **{result['emoji']} {multiplier:,.0f}K Users**: {result['tokens_burned']:,.0f} VCOIN burned ({burn_rate:.1f}%)")
        
        # Scaling analysis
        st.markdown("---")
        st.subheader("📊 Economy Scaling Analysis")
        
        # Calculate scaling ratios
        base_result = results[0]  # 1K users baseline
        
        scaling_analysis = []
        for result in results:
            user_multiplier = result['users'] / base_result['users']
            token_multiplier = result['tokens_minted'] / base_result['tokens_minted'] if base_result['tokens_minted'] > 0 else 1
            content_multiplier = result['daily_content'] / base_result['daily_content']
            reward_multiplier = result['enhanced_reward_per_content'] / base_result['enhanced_reward_per_content'] if base_result['enhanced_reward_per_content'] > 0 else 1
            
            scaling_analysis.append({
                'phase': result['emoji'] + ' ' + result['phase_name'],
                'user_scale': f"{user_multiplier:.0f}×",
                'token_generation_scale': f"{token_multiplier:.1f}×",
                'content_scale': f"{content_multiplier:.1f}×", 
                'per_content_reward_scale': f"{reward_multiplier:.2f}×",
                'economy_efficiency': f"{result['economy_health']:.0f}/100"
            })
        
        scaling_df = pd.DataFrame(scaling_analysis)
        st.table(scaling_df)
        
        # Key insights
        st.markdown("---")
        st.subheader("💡 Key Economic Insights")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🚀 Scaling Patterns:**")
            
            # Token generation scaling
            token_scale_1k_to_10k = results[1]['tokens_minted'] / results[0]['tokens_minted'] if results[0]['tokens_minted'] > 0 else 1
            token_scale_10k_to_100k = results[2]['tokens_minted'] / results[1]['tokens_minted'] if results[1]['tokens_minted'] > 0 else 1
            token_scale_100k_to_1m = results[3]['tokens_minted'] / results[2]['tokens_minted'] if results[2]['tokens_minted'] > 0 else 1
            
            st.write(f"• **1K → 10K Users**: {token_scale_1k_to_10k:.1f}× token generation")
            st.write(f"• **10K → 100K Users**: {token_scale_10k_to_100k:.1f}× token generation")
            st.write(f"• **100K → 1M Users**: {token_scale_100k_to_1m:.1f}× token generation")
            
            # Per-content reward evolution
            reward_1k = results[0]['enhanced_reward_per_content']
            reward_10k = results[1]['enhanced_reward_per_content']
            reward_100k = results[2]['enhanced_reward_per_content']
            reward_1m = results[3]['enhanced_reward_per_content']
            
            st.markdown("**💰 Per-Content Rewards:**")
            st.write(f"• **1K Users**: {reward_1k:,.0f} VCOIN (${reward_1k * vcoin_price:,.2f})")
            st.write(f"• **10K Users**: {reward_10k:,.0f} VCOIN (${reward_10k * vcoin_price:,.2f})")
            st.write(f"• **100K Users**: {reward_100k:,.0f} VCOIN (${reward_100k * vcoin_price:,.2f})")
            st.write(f"• **1M Users**: {reward_1m:,.0f} VCOIN (${reward_1m * vcoin_price:,.2f})")
        
        with col2:
            st.markdown("**⚖️ Economy Health Trends:**")
            
            # Show economy health progression
            for result in results:
                health = result['economy_health']
                if health >= 80:
                    health_status = "🎉 Excellent"
                elif health >= 60:
                    health_status = "⚠️ Good"
                else:
                    health_status = "❌ Needs Work"
                
                st.write(f"• **{result['users']:,} Users**: {health_status} ({health:.0f}/100)")
            
            # Net flow analysis
            st.markdown("**🔄 Token Flow Analysis:**")
            for result in results:
                flow_type = "📈 Inflationary" if result['net_token_flow'] > 0 else "📉 Deflationary"
                flow_rate = abs(result['net_token_flow'] / result['tokens_minted']) * 100 if result['tokens_minted'] > 0 else 0
                st.write(f"• **{result['users']:,} Users**: {flow_type} ({flow_rate:.1f}%)")
        
        # Store results for export
        st.session_state.economy_scale_results = {
            'platform_model': platform_model,
            'revenue_mode': revenue_mode,
            'vcoin_price': vcoin_price,
            'parameters': {
                'revenue_per_1k_users': revenue_per_1k_users if revenue_mode == 'revenue_backed' else 0,
                'tokens_per_content': tokens_per_content if revenue_mode == 'bootstrap_mode' else 0,
                'nft_mint_multiplier': nft_mint_multiplier if revenue_mode == 'bootstrap_mode' else 0,
                'nft_content_percentage': nft_content_percentage if revenue_mode == 'bootstrap_mode' else 0,
                'creator_percentage': creator_percentage,
                'posts_per_creator': posts_per_creator,
                'total_supply': total_supply
            },
            'phase_results': results,
            'scaling_analysis': scaling_analysis
        }
    
    # Export functionality
    if st.button("📄 Export Economy Scale Analysis", width="stretch"):
        if 'economy_scale_results' in st.session_state:
            data = st.session_state.economy_scale_results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            export_content = f"""VCOIN ECONOMY SCALE SIMULATOR REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== ANALYSIS PARAMETERS ===
Platform Model: {data['platform_model'].replace('_', ' ').title()}
Revenue Mode: {data['revenue_mode'].replace('_', ' ').title()}
VCOIN Price: ${data['vcoin_price']:.7f}
Creator Percentage: {data['parameters']['creator_percentage']}%
Posts per Creator: {data['parameters']['posts_per_creator']}

=== PLATFORM ENGAGEMENT RATIOS ===
{platform_ratios[platform_model]['description']}
- View → Like: {platform_ratios[platform_model]['view_to_like']:.1%}
- Like → Comment: {platform_ratios[platform_model]['like_to_comment']:.1%}  
- Like → Share: {platform_ratios[platform_model]['like_to_share']:.1%}

=== PHASE-BY-PHASE ANALYSIS ===
"""
            
            for result in data['phase_results']:
                export_content += f"""
{result['emoji']} {result['phase_name'].upper()} - {result['users']:,} USERS:

User Metrics:
- Active Users: {result['users']:,}
- Daily Creators: {result['creators']:,}
- Daily Content: {result['daily_content']:,} pieces
- Total Daily Views: {result['total_views']:,}
- Total Daily Likes: {result['total_likes']:,}
- Total Daily Comments: {result['total_comments']:,}
- Total Daily Shares: {result['total_shares']:,}
- Overall Engagement Rate: {result['engagement_rate']:.1%}

Token Economics:
- Daily Revenue: ${result['daily_revenue']:,.0f}
- Reward Pool: {result['reward_pool_tokens']:,.0f} VCOIN (${result['reward_pool_usd']:,.0f})
- Base Reward per Content: {result['base_reward_per_content']:,.0f} VCOIN
- Enhanced Reward per Content: {result['enhanced_reward_per_content']:,.0f} VCOIN (${result['enhanced_reward_per_content'] * data['vcoin_price']:,.2f})
- Total Content Rewards: {result['total_content_rewards']:,.0f} VCOIN

Token Flow:
- Daily Minted: {result['tokens_minted']:,.0f} VCOIN
- Daily Burned: {result['tokens_burned']:,.0f} VCOIN  
- Net Flow: {result['net_token_flow']:+,.0f} VCOIN ({'Inflationary' if result['net_token_flow'] > 0 else 'Deflationary'})
- Economy Health: {result['economy_health']:.0f}/100

Content Distribution:
"""
                
                for scenario in result['content_scenarios']:
                    export_content += f"""- {scenario['type'].title()}: {scenario['count']} pieces | {scenario['views']:,} views | {scenario['likes']:,} likes | {scenario['comments']:,} comments | {scenario['shares']:,} shares
"""
            
            export_content += f"""
=== SCALING ANALYSIS SUMMARY ===

VCOIN Generation by User Scale:
- 1K Users: {results[0]['tokens_minted']:,.0f} VCOIN/day
- 10K Users: {results[1]['tokens_minted']:,.0f} VCOIN/day ({results[1]['tokens_minted']/results[0]['tokens_minted']:.1f}× increase)
- 100K Users: {results[2]['tokens_minted']:,.0f} VCOIN/day ({results[2]['tokens_minted']/results[0]['tokens_minted']:.1f}× increase)  
- 1M Users: {results[3]['tokens_minted']:,.0f} VCOIN/day ({results[3]['tokens_minted']/results[0]['tokens_minted']:.1f}× increase)

Per-Content Reward Evolution:
- 1K Users: {results[0]['enhanced_reward_per_content']:,.0f} VCOIN per content
- 10K Users: {results[1]['enhanced_reward_per_content']:,.0f} VCOIN per content
- 100K Users: {results[2]['enhanced_reward_per_content']:,.0f} VCOIN per content
- 1M Users: {results[3]['enhanced_reward_per_content']:,.0f} VCOIN per content

Economy Health Progression:
- 1K Users: {results[0]['economy_health']:.0f}/100
- 10K Users: {results[1]['economy_health']:.0f}/100  
- 100K Users: {results[2]['economy_health']:.0f}/100
- 1M Users: {results[3]['economy_health']:.0f}/100

Key Insights:
- Token generation scales {results[3]['tokens_minted']/results[0]['tokens_minted']:.0f}× from 1K to 1M users
- Per-content rewards {'increase' if results[3]['enhanced_reward_per_content'] > results[0]['enhanced_reward_per_content'] else 'decrease'} with scale
- Economy health {'improves' if results[3]['economy_health'] > results[0]['economy_health'] else 'declines'} at larger scales
- Platform is {'sustainable' if all(r['net_token_flow'] < r['tokens_minted'] * 0.2 for r in results) else 'needs balancing'} across all phases
"""
            
            st.download_button(
                label="📄 Download Economy Scale Report",
                data=export_content,
                file_name=f"vcoin_economy_scale_analysis_{timestamp}.txt",
                mime="text/plain",
                width="stretch"
            )
        else:
            st.warning("⚠️ Please run the analysis first before exporting")

def content_calculator_interface():
    """Individual content reward calculator"""
    
    st.header("🎬 Individual Content Reward Calculator")
    st.markdown("Calculate VCOIN rewards for specific content pieces")
    
    # Add platform parameters section at the top
    st.subheader("🏢 Platform Economics Parameters")
    st.markdown("**Adjust the base economic parameters that affect all content rewards**")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        daily_revenue = st.number_input(
            "Daily Platform Revenue ($)", 
            min_value=0, max_value=1_000_000, value=50_000, step=1000,
            help="💡 Total daily revenue from ads, subscriptions, and other sources (set to $0 for bootstrap mode)"
        )
    
    with col2:
        revenue_share_percent = st.slider(
            "Revenue Share for Rewards (%)", 
            min_value=50, max_value=90, value=70, step=5,
            help="💡 Percentage of daily revenue allocated to creator and user rewards"
        )
    
    with col3:
        daily_active_users = st.number_input(
            "Daily Active Users", 
            min_value=1000, max_value=10_000_000, value=100_000, step=5000,
            help="💡 Number of users actively engaging with content daily"
        )
    
    # VCOIN Price Input
    st.markdown("**💰 VCOIN Token Price**")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Enhanced token price input with dropdown + custom
        common_prices = ["0.0000001", "0.00001", "0.0001", "0.001", "0.01", "0.10", "1.00"]
        dropdown_options = common_prices + ["Custom..."]
        selected_option = st.selectbox(
            "Select or enter VCOIN price:",
            dropdown_options,
            index=5,  # Default to $0.10
            key="vcoin_price_dropdown_content",
            help="💡 Current VCOIN token price for USD calculations"
        )
    
    with col2:
        if selected_option == "Custom...":
            custom_price = st.text_input("Custom Price:", value="0.10", key="custom_vcoin_price_content")
            try:
                vcoin_price = float(custom_price)
                if vcoin_price <= 0:
                    st.error("⚠️ Must be > 0")
                    vcoin_price = 0.10
            except ValueError:
                st.error("⚠️ Invalid")
                vcoin_price = 0.10
        else:
            vcoin_price = float(selected_option)
            st.write("")
    
    st.success(f"💰 VCOIN Price: ${vcoin_price:.7f}")
    
    # Calculate and display base pool
    if daily_revenue > 0:
        base_pool_total = daily_revenue * (revenue_share_percent / 100)
        base_pool_per_user = base_pool_total / daily_active_users
        
        st.info(f"""
        **📊 Revenue-Backed Reward Pool:**
        - Daily Revenue: ${daily_revenue:,}
        - Revenue Share: {revenue_share_percent}% = ${base_pool_total:,.0f}
        - Per User Pool: ${base_pool_total:,.0f} ÷ {daily_active_users:,} = ${base_pool_per_user:.4f} per user
        """)
    else:
        # Bootstrap mode parameters
        st.markdown("**🚀 Bootstrap Mode Configuration**")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            daily_token_mint_rate = st.slider("Daily Token Mint Rate (%)", 
                                            min_value=0.01, max_value=1.0, value=0.1, step=0.01,
                                            help="💡 Daily % of total supply minted for rewards")
        
        with col2:
            total_token_supply = st.number_input("Total Token Supply", 
                                               min_value=1_000_000, max_value=50_000_000_000, value=1_000_000_000, step=1_000_000,
                                               help="💡 Total VCOIN supply for mint calculations")
        
        daily_token_mint = total_token_supply * (daily_token_mint_rate / 100)
        base_pool_per_user = daily_token_mint / daily_active_users
        
        st.success(f"""
        **🪙 Bootstrap Mode - Token-Only Rewards:**
        - Total Supply: {total_token_supply:,} VCOIN
        - Daily Mint: {daily_token_mint_rate}% = {daily_token_mint:,.0f} VCOIN
        - Per User Pool: {daily_token_mint:,.0f} ÷ {daily_active_users:,} = {base_pool_per_user:.2f} VCOIN per user
        - USD Equivalent: {base_pool_per_user:.2f} VCOIN × ${vcoin_price:.7f} = ${base_pool_per_user * vcoin_price:.4f} per user
        """)
    
    with st.expander("💡 Economic Model Explanation", expanded=False):
        if daily_revenue > 0:
            st.markdown(f"""
            **🏢 Revenue-Supported Model:**
            
            **Daily Revenue Sources:**
            - 📺 Advertising revenue (CPM from sponsors)
            - 💳 Premium subscriptions 
            - 🛒 In-app purchases and tips
            - 🤝 Partnership and affiliate income
            
            **Revenue Share ({revenue_share_percent}%):**
            - **{revenue_share_percent}% to Rewards**: Competitive with YouTube (55%), TikTok (50%), Twitch (50-70%)
            - **{100-revenue_share_percent}% to Platform**: Operations, development, marketing, infrastructure, profit
            - **Why {revenue_share_percent}%?** Attracts top creators while maintaining platform viability
            
            **User Distribution:**
            - **{daily_active_users:,} Daily Users**: Ensures fair distribution across user base
            - **Scalable Model**: Rewards grow with platform revenue and user base
            """)
        else:
            st.markdown(f"""
            **🚀 Bootstrap Mode - No Revenue Required:**
            
            **Token Minting Strategy:**
            - **No external revenue** needed to reward users
            - **Controlled inflation**: {daily_token_mint_rate}% daily mint rate
            - **Community building**: Early adopters earn tokens that gain value
            - **Sustainable launch**: No cash burn while building user base
            
            **Economic Logic:**
            - **Early Rewards**: Users get tokens when platform has no revenue
            - **Value Creation**: Token utility and demand increase with user growth
            - **Network Effects**: More users → higher token value → better rewards
            - **Transition Ready**: Can add revenue backing later
            
            **Sustainability:**
            - **{daily_token_mint_rate}% daily** = {daily_token_mint_rate * 365:.1f}% annual inflation
            - **User growth** typically exceeds inflation rate
            - **Future revenue** can reduce minting dependency
            """)
    
    st.divider()
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Content Details")
        
        content_type = st.selectbox(
            "Content Type", 
            ['podcast', 'long_video', 'short_video', 'text_post'],
            format_func=lambda x: {
                'podcast': '🎙️ Podcast',
                'long_video': '📹 Long Video', 
                'short_video': '📱 Short Video',
                'text_post': '📝 Text Post'
            }[x]
        )
        
        view_count = st.number_input("View Count", 10, 1_000_000, 1000)
        
        if content_type in ['podcast', 'long_video']:
            duration = st.number_input("Duration (minutes)", 1, 180, 30)
        elif content_type == 'short_video':
            duration = st.number_input("Duration (seconds)", 15, 300, 60) / 60
        else:
            duration = 0
        
        st.subheader("👥 Engagement Metrics")
        
        # Platform selection for realistic benchmarks
        platform_type = st.selectbox(
            "📱 Platform Type (affects defaults)",
            ['new_crypto_app', 'tiktok_like', 'youtube_like', 'instagram_like', 'twitter_like', 'custom'],
            format_func=lambda x: {
                'new_crypto_app': '🪙 New Crypto Social App (Conservative)',
                'tiktok_like': '🎵 TikTok-like (High Engagement)',
                'youtube_like': '📺 YouTube-like (Moderate)',
                'instagram_like': '📸 Instagram-like (Low-Med)',
                'twitter_like': '🐦 Twitter-like (Low)',
                'custom': '⚙️ Custom Values'
            }[x],
            help="💡 Select platform type to auto-populate realistic engagement defaults based on 2024-2025 industry benchmarks"
        )
        
        # Define engagement benchmarks based on research
        engagement_benchmarks = {
            'new_crypto_app': {
                'base_rate': 0.015,  # 1.5% - Conservative for new platforms
                'shares_ratio': 0.08,   # 8% of engagement (lower for new platforms)
                'likes_ratio': 0.60,    # 60% of engagement 
                'dislikes_ratio': 0.12, # 12% of engagement (higher controversy tolerance)
                'comments_ratio': 0.20, # 20% of engagement (higher discussion)
                'description': "Conservative estimates for new crypto/Web3 platforms with smaller, engaged communities"
            },
            'tiktok_like': {
                'base_rate': 0.025,  # 2.5% - Based on 2025 TikTok benchmarks
                'shares_ratio': 0.15,   # 15% of engagement
                'likes_ratio': 0.70,    # 70% of engagement
                'dislikes_ratio': 0.05, # 5% of engagement
                'comments_ratio': 0.10, # 10% of engagement
                'description': "High engagement typical of short-form video platforms like TikTok"
            },
            'youtube_like': {
                'base_rate': 0.044,  # 4.4% - Based on YouTube 2025 benchmarks
                'shares_ratio': 0.05,   # 5% of engagement
                'likes_ratio': 0.75,    # 75% of engagement
                'dislikes_ratio': 0.05, # 5% of engagement
                'comments_ratio': 0.15, # 15% of engagement
                'description': "Moderate engagement typical of long-form video platforms like YouTube"
            },
            'instagram_like': {
                'base_rate': 0.0116,  # 1.16% - Based on Instagram 2025 benchmarks
                'shares_ratio': 0.08,   # 8% of engagement
                'likes_ratio': 0.80,    # 80% of engagement
                'dislikes_ratio': 0.02, # 2% of engagement
                'comments_ratio': 0.10, # 10% of engagement
                'description': "Lower engagement typical of photo-sharing platforms like Instagram"
            },
            'twitter_like': {
                'base_rate': 0.0231,  # 2.31% - Based on X/Twitter 2025 benchmarks
                'shares_ratio': 0.25,   # 25% of engagement (retweets)
                'likes_ratio': 0.60,    # 60% of engagement
                'dislikes_ratio': 0.05, # 5% of engagement
                'comments_ratio': 0.10, # 10% of engagement
                'description': "Text-focused platform with high sharing, moderate likes"
            },
            'custom': {
                'base_rate': 0.02,   # 2% default
                'shares_ratio': 0.10,
                'likes_ratio': 0.65,
                'dislikes_ratio': 0.10,
                'comments_ratio': 0.15,
                'description': "Custom values - set your own engagement patterns"
            }
        }
        
        benchmark = engagement_benchmarks[platform_type]
        
        # Content-type multipliers based on industry data (define before use)
        content_multipliers = {
            'short_video': 1.8,    # Short videos get 80% higher engagement
            'long_video': 1.2,     # Long videos get 20% higher engagement  
            'podcast': 0.8,        # Podcasts get 20% lower visual engagement
            'text_post': 0.6       # Text posts get 40% lower engagement
        }
        
        content_mult = content_multipliers.get(content_type, 1.0)
        
        # Show benchmark info with content type adjustment
        adjusted_rate = benchmark['base_rate'] * content_mult
        st.info(f"""
        **📊 {platform_type.replace('_', ' ').title()} + {content_type.replace('_', ' ').title()} Benchmarks:**
        - **Base Engagement Rate**: {benchmark['base_rate']:.1%} × {content_mult:.1f} = {adjusted_rate:.1%} of views
        - **Content Type Impact**: {content_type.replace('_', ' ').title()} gets {(content_mult-1)*100:+.0f}% engagement vs average
        - **Platform Rationale**: {benchmark['description']}
        - **Expected Engagement**: ~{int(view_count * adjusted_rate):,} total interactions for {view_count:,} views
        - **Source**: Industry benchmarks from Buffer, Hootsuite, Social Insider (2024-2025)
        """)
        
        # Calculate engagement defaults based on selected benchmark and content type
        if platform_type != 'custom':
            base_engagement = view_count * benchmark['base_rate'] * content_mult
            total_engagement = int(base_engagement)
            default_shares = max(1, int(total_engagement * benchmark['shares_ratio']))
            default_likes = max(1, int(total_engagement * benchmark['likes_ratio']))
            default_dislikes = max(0, int(total_engagement * benchmark['dislikes_ratio']))
            default_comments = max(1, int(total_engagement * benchmark['comments_ratio']))
        else:
            # Custom defaults
            base_engagement = view_count * 0.02 * content_mult
            total_engagement = int(base_engagement)
            default_shares = max(1, int(total_engagement * 0.10))
            default_likes = max(1, int(total_engagement * 0.65))
            default_dislikes = max(0, int(total_engagement * 0.10))
            default_comments = max(1, int(total_engagement * 0.15))
        
        shares = st.number_input(
            "Shares/Reposts", 0, view_count//2, default_shares,
            help=f"💡 Default: {benchmark['shares_ratio']:.0%} of total engagement ({default_shares:,} for {view_count:,} views)"
        )
        likes = st.number_input(
            "Likes", 0, view_count, default_likes,
            help=f"💡 Default: {benchmark['likes_ratio']:.0%} of total engagement ({default_likes:,} for {view_count:,} views)"
        )
        dislikes = st.number_input(
            "Dislikes", 0, view_count//5, default_dislikes,
            help=f"💡 Default: {benchmark['dislikes_ratio']:.0%} of total engagement ({default_dislikes:,} for {view_count:,} views)"
        )
        comments = st.number_input(
            "Comments", 0, view_count//3, default_comments,
            help=f"💡 Default: {benchmark['comments_ratio']:.0%} of total engagement ({default_comments:,} for {view_count:,} views)"
        )
        
        # Total viewers (replaces reports)
        total_viewers = st.number_input("Total Viewers", 1, view_count * 3, view_count, 
                                      help="💡 Total unique viewers who watched the content")
        
        # Show engagement reality check for new crypto platforms
        if platform_type == 'new_crypto_app':
            actual_engagement_rate = (shares + likes + dislikes + comments) / max(1, view_count)
            st.warning(f"""
            **🚨 New Crypto Platform Reality Check:**
            
            **Current Engagement**: {actual_engagement_rate:.1%} of views
            **Benchmark Range**: 0.5% - 3.0% (typical for new platforms)
            
            **Why Lower Engagement is Normal:**
            - **Small User Base**: Fewer active users = lower absolute engagement
            - **Learning Curve**: Users still discovering platform features
            - **Crypto Barrier**: Not everyone comfortable with crypto rewards yet
            - **Content Discovery**: Algorithm still learning user preferences
            - **Network Effects**: Engagement grows exponentially with user base
            
            **Growth Trajectory**: Most successful platforms start at 0.5-1.5% and grow to 3-5% within 12-18 months.
            """)
        
        # Show engagement composition analysis
        total_user_engagement = shares + likes + dislikes + comments
        if total_user_engagement > 0:
            st.success(f"""
            **📈 Engagement Breakdown Analysis:**
            - **Total Interactions**: {total_user_engagement:,} ({total_user_engagement/view_count:.1%} of views)
            - **Shares**: {shares:,} ({shares/total_user_engagement:.1%} of engagement)
            - **Likes**: {likes:,} ({likes/total_user_engagement:.1%} of engagement) 
            - **Dislikes**: {dislikes:,} ({dislikes/total_user_engagement:.1%} of engagement)
            - **Comments**: {comments:,} ({comments/total_user_engagement:.1%} of engagement)
            - **Engagement Quality**: {'High' if total_user_engagement/view_count > 0.03 else 'Moderate' if total_user_engagement/view_count > 0.015 else 'Building'}
            """)
        
        st.subheader("⭐ Quality Scores")
        creator_5a = st.slider("Creator 5A Score (%)", 1, 100, 75, help="Authority, Accuracy, Authenticity, Audience, Amplification (1-100%)")
        accuracy = st.slider("Content Accuracy %", 0, 100, 80, help="Community-verified accuracy rating")
        engagement_quality = st.slider("Engagement Quality", 0, 100, 70, help="Quality of user interactions")
    
    with col2:
        st.subheader("💰 Reward Calculation")
        
        if st.button("🧮 Calculate Rewards", type="primary"):
            
            # Convert 5A score from 1-100% to engine's expected 100-500 range
            adjusted_5a_score = (creator_5a / 100) * 400 + 100
            
            # Calculate engagement multiplier based on engagement metrics
            # Higher engagement = higher total reward (likes and dislikes treated equally)
            total_reactions = likes + dislikes
            engagement_rate = (shares + total_reactions + comments) / max(1, view_count)
            engagement_multiplier = 1.0 + (engagement_rate * 2.0)  # Up to 3x multiplier for high engagement
            
            # No separate dislike penalty - all reactions are treated as engagement
            final_engagement_multiplier = engagement_multiplier
            
            # Create content metrics object
            content_metrics = ContentMetrics(
                content_type=content_type,
                view_count=view_count,
                shares=shares,
                reports=0,  # No longer used
                likes=likes,
                dislikes=dislikes,
                comments=comments,
                creator_5a_score=adjusted_5a_score,  # Use adjusted score
                accuracy_rating=accuracy,
                engagement_quality=engagement_quality,
                duration_minutes=duration
            )
            
            # Initialize engine with user-adjusted parameters
            if daily_revenue > 0:
                engine_params = {
                    'daily_revenue': daily_revenue,
                    'daily_users': daily_active_users,
                    'initial_price': vcoin_price,
                    'revenue_share_percent': revenue_share_percent
                }
            else:
                # Bootstrap mode - use token minting for rewards
                engine_params = {
                    'daily_revenue': daily_token_mint * vcoin_price,  # Convert tokens to USD equivalent at user price
                    'daily_users': daily_active_users,
                    'initial_price': vcoin_price,
                    'revenue_share_percent': 100,  # 100% of "revenue" goes to rewards in bootstrap
                    'bootstrap_mode': True,
                    'daily_token_mint': daily_token_mint
                }
            engine = VCoinEconomicEngine(engine_params)
            
            # Calculate rewards
            base_reward_result = engine.calculate_content_reward(content_metrics)
            
            # Apply engagement multiplier to total reward
            total_vcoin_base = base_reward_result['total_reward']
            total_vcoin = total_vcoin_base * final_engagement_multiplier
            total_usd = total_vcoin * vcoin_price  # At user-specified VCOIN price
            
            # Display total reward with engagement impact
            st.success("✅ Reward Calculation Complete")
            
            # Show engagement impact
            st.info(f"""
            **📊 Engagement Impact Analysis:**
            - Base Reward: {total_vcoin_base:,.0f} VCOIN
            - Engagement Rate: {engagement_rate:.1%} (shares + reactions + comments / views)
            - Engagement Multiplier: {engagement_multiplier:.2f}x
            - **Final Multiplier: {final_engagement_multiplier:.2f}x**
            - **Total Reward: {total_vcoin:,.0f} VCOIN** (${total_usd:,.2f})
            
            **Note**: Likes and dislikes are treated equally as engagement signals
            """)
            
            st.metric("💎 Total Content Reward", f"{total_vcoin:,.0f} VCOIN", f"${total_usd:,.2f}")
            
            # Distribution breakdown
            st.subheader("💸 Reward Distribution")
            
            # Recalculate distribution with new total and viewer rewards
            creator_reward = total_vcoin * 0.40  # 40% to creator
            share_reward_pool = total_vcoin * 0.20  # 20% to sharers
            viewer_reward_pool = total_vcoin * 0.075  # 7.5% to viewers
            reaction_reward_pool = total_vcoin * 0.10  # 10% to reactions (likes + dislikes combined)
            comment_reward_pool = total_vcoin * 0.125  # 12.5% to commenters
            platform_commission = total_vcoin * 0.10  # 10% to platform
            
            distribution_data = {
                'Recipient': [
                    '👤 Creator',
                    '🔄 Sharers', 
                    '👀 Viewers',
                    '👍👎 Reactions (Likes + Dislikes)',
                    '💬 Commenters',
                    '🏢 ViWo Commission'
                ],
                'VCOIN Amount': [
                    f"{creator_reward:,.0f}",
                    f"{share_reward_pool:,.0f}",
                    f"{viewer_reward_pool:,.0f}",
                    f"{reaction_reward_pool:,.0f}",
                    f"{comment_reward_pool:,.0f}",
                    f"{platform_commission:,.0f}"
                ],
                'USD Value': [
                    f"${creator_reward * vcoin_price:,.2f}",
                    f"${share_reward_pool * vcoin_price:,.2f}",
                    f"${viewer_reward_pool * vcoin_price:,.2f}",
                    f"${reaction_reward_pool * vcoin_price:,.2f}",
                    f"${comment_reward_pool * vcoin_price:,.2f}",
                    f"${platform_commission * vcoin_price:,.2f}"
                ],
                'Percentage': [
                    "40.0%", "20.0%", "7.5%", "10.0%", "12.5%", "10.0%"
                ]
            }
            
            dist_df = pd.DataFrame(distribution_data)
            st.table(dist_df)
            
            # Individual user rewards
            if shares + total_viewers + likes + dislikes + comments > 0:
                st.subheader("👤 Individual User Rewards")
                
                # Calculate per-action rewards
                share_per_action = share_reward_pool / max(1, shares)
                viewer_per_action = viewer_reward_pool / max(1, total_viewers)
                total_reactions = likes + dislikes
                reaction_per_action = reaction_reward_pool / max(1, total_reactions)
                comment_per_action = comment_reward_pool / max(1, comments)
                
                individual_data = {
                    'Action': ['🔄 Share', '👀 View', '👍👎 Reaction (Like/Dislike)', '💬 Comment'],
                    'Count': [shares, total_viewers, total_reactions, comments],
                    'Reward per Action': [
                        f"{share_per_action:,.3f} VCOIN" if shares > 0 else "0 VCOIN",
                        f"{viewer_per_action:,.3f} VCOIN" if total_viewers > 0 else "0 VCOIN",
                        f"{reaction_per_action:,.3f} VCOIN" if total_reactions > 0 else "0 VCOIN",
                        f"{comment_per_action:,.3f} VCOIN" if comments > 0 else "0 VCOIN"
                    ],
                    'USD per Action': [
                        f"${share_per_action * vcoin_price:,.3f}" if shares > 0 else "$0.000",
                        f"${viewer_per_action * vcoin_price:,.3f}" if total_viewers > 0 else "$0.000",
                        f"${reaction_per_action * vcoin_price:,.3f}" if total_reactions > 0 else "$0.000",
                        f"${comment_per_action * vcoin_price:,.3f}" if comments > 0 else "$0.000"
                    ]
                }
                
                individual_df = pd.DataFrame(individual_data)
                st.table(individual_df)
                
                # Quality impact analysis
                st.subheader("📈 Quality Impact Analysis")
                
                quality_factors = {
                    'Base Content Multiplier': f"{engine.content_multipliers[content_type]}x",
                    'Creator 5A Score': f"{creator_5a}% (converted to {adjusted_5a_score:.0f} for calculation)",
                    'Creator 5A Multiplier': f"{engine._calculate_quality_multiplier(content_metrics):.2f}x",
                    'Accuracy Bonus': f"{((accuracy/100) * 0.20 + 1):.2f}x",
                    'Final Quality Multiplier': f"{engine._calculate_quality_multiplier(content_metrics):.2f}x"
                }
                
                for factor, value in quality_factors.items():
                    st.write(f"**{factor}:** {value}")
            
            # Formula explanation section
            st.subheader("🧮 Calculation Formula Breakdown")
            
            with st.expander("📐 Complete Formula Explanation", expanded=False):
                st.markdown("""
                ### **VCOIN Content Reward Calculation Formula**
                
                #### **Step 1: Base Reward Pool**
                """)
                
                if daily_revenue > 0:
                    st.markdown(f"""
                    ```
                    Revenue-Backed Model:
                    Base Pool = (Daily Revenue × Revenue Share %) ÷ Daily Active Users
                    Base Pool = (${daily_revenue:,} × {revenue_share_percent}%) ÷ {daily_active_users:,} = ${base_pool_per_user:.4f} per user
                    ```""")
                else:
                    st.markdown(f"""
                    ```
                    Bootstrap Mode (Token-Only):
                    Base Pool = (Total Supply × Daily Mint Rate %) ÷ Daily Active Users
                    Base Pool = ({total_token_supply:,} × {daily_token_mint_rate}%) ÷ {daily_active_users:,} = {base_pool_per_user:.2f} VCOIN per user
                    ```""")
                
                st.markdown("""
                
                **📊 Why This Formula:**""")
                
                if daily_revenue > 0:
                    st.markdown(f"""
                    **🏢 Revenue-Backed Model:**
                    - **Daily Revenue (${daily_revenue:,})**: Platform's total daily income from:
                      - 📺 Advertising revenue (CPM from sponsors)
                      - 💳 Premium subscriptions 
                      - 🛒 In-app purchases and tips
                      - 🤝 Partnership and affiliate income
                    
                    - **Revenue Share ({revenue_share_percent}%)**: Portion allocated to rewards because:
                      - 🎯 **Incentivizes quality content creation**
                      - 🔄 **Encourages user engagement and retention**
                      - ⚖️ **Balances platform sustainability vs user rewards**
                      - 📈 **Creates positive feedback loop for growth**
                      - Remaining {100-revenue_share_percent}% covers: operations, development, marketing, profit
                    
                    **💡 Economic Impact:**
                    - Higher revenue → Larger reward pools → Better creator incentives
                    - More users → Distributed rewards → Sustainable growth model
                    - Optimal revenue share → Platform viability + user satisfaction""")
                else:
                    st.markdown(f"""
                    **🚀 Bootstrap Mode (No Revenue Required):**
                    - **Total Supply ({total_token_supply:,} VCOIN)**: Available tokens for minting rewards
                    - **Daily Mint Rate ({daily_token_mint_rate}%)**: Controlled inflation for sustainability:
                      - 🎯 **Rewards early adopters** without cash requirements
                      - 🔄 **Builds community** before monetization
                      - ⚖️ **Prevents hyperinflation** with reasonable rates
                      - 📈 **Creates token utility** and demand through usage
                    
                    **💡 Bootstrap Benefits:**
                    - No revenue needed → Immediate launch capability
                    - Token rewards → Community building and retention  
                    - User growth → Token value appreciation
                    - Transition ready → Can add revenue backing later""")
                
                st.markdown(f"""
                
                - **Daily Active Users ({daily_active_users:,})**: Reward pool distribution base because:
                  - 👥 **Ensures fair distribution across user base**
                  - 📊 **Scales rewards with platform growth**
                  - 💰 **Maintains consistent per-user economics**
                  - 🎯 **Prevents reward dilution as platform grows**
                
                #### **Step 2: Content Type Multiplier**
                ```
                Content Multipliers:
                • 🎙️ Podcast: 2.5x
                • 📹 Long Video: 2.0x  
                • 📱 Short Video: 1.0x
                • 📝 Text Post: 0.8x
                
                Adjusted Pool = Base Pool × Content Multiplier
                ```
                
                #### **Step 3: 5A Quality Multiplier**
                ```
                5A Multiplier = (5A Score ÷ 100) × 2.0 + 0.5
                
                Example: 75% 5A Score
                5A Multiplier = (75 ÷ 100) × 2.0 + 0.5 = 2.0x
                ```
                
                #### **Step 4: Accuracy Bonus**
                ```
                Accuracy Bonus = (Accuracy % ÷ 100) × 0.20 + 1.0
                
                Example: 80% Accuracy
                Accuracy Bonus = (80 ÷ 100) × 0.20 + 1.0 = 1.16x
                ```
                
                #### **Step 5: View Count Impact**
                ```
                View Multiplier = log10(View Count) ÷ 3.0
                
                Example: 1,000 views
                View Multiplier = log10(1000) ÷ 3.0 = 1.0x
                ```
                
                #### **Step 6: Total Content Reward**
                ```
                Total Reward = Base Pool × Content Multiplier × 5A Multiplier × 
                              Accuracy Bonus × View Multiplier × View Count
                ```
                
                #### **Step 7: Engagement Multiplier (UPDATED!)**
                ```
                Total Reactions = Likes + Dislikes (treated equally)
                Engagement Rate = (Shares + Total Reactions + Comments) ÷ Views
                Engagement Multiplier = 1.0 + (Engagement Rate × 2.0)  [Max 3.0x]
                
                Enhanced Total = Base Reward × Engagement Multiplier
                ```
                
                #### **Step 8: Distribution Breakdown (UPDATED!)**
                ```
                • Creator (40%): Enhanced Total × 0.40
                • Engagement Pool (50%):
                  - Shares (20%): Enhanced Total × 0.20 ÷ Share Count
                  - Viewers (7.5%): Enhanced Total × 0.075 ÷ Total Viewers
                  - Reactions (10%): Enhanced Total × 0.10 ÷ (Likes + Dislikes)
                  - Comments (12.5%): Enhanced Total × 0.125 ÷ Comment Count
                • ViWo Commission (10%): Enhanced Total × 0.10
                ```
                
                #### **Current Calculation:**
                """)
                
                # Show actual calculation with current values
                base_pool = (engine_params['daily_revenue'] * 0.7) / engine_params['daily_users']
                content_mult = engine.content_multipliers[content_type]
                
                # Convert 5A score from 1-100 to the engine's expected format
                adjusted_5a_score = (creator_5a / 100) * 400 + 100  # Convert 1-100% to 100-500 range
                
                # Create adjusted content metrics for calculation
                adjusted_content_metrics = ContentMetrics(
                    content_type=content_type,
                    view_count=view_count,
                    shares=shares,
                    reports=0,  # No longer used
                    likes=likes,
                    dislikes=dislikes,
                    comments=comments,
                    creator_5a_score=adjusted_5a_score,  # Use adjusted score
                    accuracy_rating=accuracy,
                    engagement_quality=engagement_quality,
                    duration_minutes=duration
                )
                
                quality_mult = engine._calculate_quality_multiplier(adjusted_content_metrics)
                accuracy_bonus = (accuracy/100) * 0.20 + 1.0
                
                import math
                view_mult = math.log10(max(1, view_count)) / 3.0
                
                if daily_revenue > 0:
                    st.markdown(f"""
                    ```
                    Base Pool = ${engine_params['daily_revenue']:,.0f} × {revenue_share_percent/100:.2f} ÷ {engine_params['daily_users']:,.0f} = {base_pool:.4f} VCOIN
                    Content Multiplier = {content_mult:.1f}x ({content_type})
                    5A Multiplier = ({creator_5a} ÷ 100) × 2.0 + 0.5 = {quality_mult:.2f}x
                    Accuracy Bonus = ({accuracy} ÷ 100) × 0.20 + 1.0 = {accuracy_bonus:.2f}x
                    View Multiplier = log10({view_count:,}) ÷ 3.0 = {view_mult:.2f}x
                    ```""")
                else:
                    st.markdown(f"""
                    ```
                    Base Pool = {total_token_supply:,} × {daily_token_mint_rate/100:.3f} ÷ {engine_params['daily_users']:,.0f} = {base_pool:.2f} VCOIN
                    Content Multiplier = {content_mult:.1f}x ({content_type})
                    5A Multiplier = ({creator_5a} ÷ 100) × 2.0 + 0.5 = {quality_mult:.2f}x
                    Accuracy Bonus = ({accuracy} ÷ 100) × 0.20 + 1.0 = {accuracy_bonus:.2f}x
                    View Multiplier = log10({view_count:,}) ÷ 3.0 = {view_mult:.2f}x
                    ```""")
                
                st.markdown(f"""
                
                Base Reward = {base_pool:.4f} × {content_mult:.1f} × {quality_mult:.2f} × {accuracy_bonus:.2f} × {view_mult:.2f} × {view_count:,}
                Base Reward = {total_vcoin_base:,.0f} VCOIN
                
                Total Reactions = {likes} + {dislikes} = {total_reactions} (likes and dislikes treated equally)
                Engagement Rate = ({shares} + {total_reactions} + {comments}) ÷ {view_count} = {engagement_rate:.1%}
                Engagement Multiplier = 1.0 + ({engagement_rate:.3f} × 2.0) = {engagement_multiplier:.2f}x
                
                **Enhanced Total = {total_vcoin_base:,.0f} × {final_engagement_multiplier:.2f} = {total_vcoin:,.0f} VCOIN (${total_usd:,.2f})**
                ```
                """)
                
                # Add market context to the formula explanation
                st.markdown(f"""
                **📊 Market Context & Benchmarks:**
                - **Platform Type**: {platform_type.replace('_', ' ').title()}
                - **Industry Benchmark**: {benchmark['base_rate']:.1%} base engagement rate
                - **Content Adjustment**: {content_mult:.1f}× for {content_type.replace('_', ' ')}
                - **Actual Engagement**: {engagement_rate:.1%} vs {adjusted_rate:.1%} expected
                - **Performance**: {'Above' if engagement_rate > adjusted_rate else 'Below' if engagement_rate < adjusted_rate else 'At'} benchmark
                """)
                
                if daily_revenue > 0:
                    st.info("💡 **Revenue-Backed Model**: Rewards funded by platform revenue. Likes and dislikes both count as positive engagement.")
                else:
                    st.info(f"💡 **Bootstrap Mode**: Pure VCOIN tokens from {daily_token_mint_rate}% daily minting. All reactions (likes + dislikes) boost rewards equally!")

def ab_comparison_interface():
    """A/B testing interface for comparing parameter sets"""
    
    st.header("⚔️ A/B Parameter Comparison")
    st.markdown("Compare two different parameter configurations side-by-side")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Scenario A")
        params_a = create_parameter_inputs("a", "Current Setup")
        
    with col2:
        st.subheader("📊 Scenario B") 
        params_b = create_parameter_inputs("b", "Alternative Setup")
    
    if st.button("⚔️ Compare Scenarios", type="primary"):
        
        with st.spinner("🔄 Running A/B comparison..."):
            # Run both simulations
            results_a = run_quick_simulation(params_a, 90)  # 90-day simulation
            results_b = run_quick_simulation(params_b, 90)
            
            # Calculate comparison metrics
            comparison = compare_simulation_results(results_a, results_b)
        
        st.success("✅ A/B Comparison Complete")
        
        # Display comparison table
        st.subheader("📋 Scenario Comparison")
        
        comparison_data = {
            'Metric': [
                '💰 Final Token Price',
                '📈 Price Appreciation',
                '📊 Supply Growth', 
                '👤 Avg Creator Earnings',
                '🏢 Platform Revenue',
                '❤️ Economic Health Score'
            ],
            'Scenario A': [
                f"${comparison['scenario_a']['final_price']:.4f}",
                f"{comparison['scenario_a']['price_appreciation']:.1%}",
                f"{comparison['scenario_a']['supply_growth']:.1%}",
                f"${comparison['scenario_a']['avg_creator_earnings']:,.0f}",
                f"${comparison['scenario_a']['platform_revenue']:,.0f}",
                f"{comparison['scenario_a']['health_score']:.0f}/100"
            ],
            'Scenario B': [
                f"${comparison['scenario_b']['final_price']:.4f}",
                f"{comparison['scenario_b']['price_appreciation']:.1%}",
                f"{comparison['scenario_b']['supply_growth']:.1%}",
                f"${comparison['scenario_b']['avg_creator_earnings']:,.0f}",
                f"${comparison['scenario_b']['platform_revenue']:,.0f}",
                f"{comparison['scenario_b']['health_score']:.0f}/100"
            ],
            'Winner': comparison['winners']
        }
        
        comp_df = pd.DataFrame(comparison_data)
        st.table(comp_df)
        
        # Overall recommendation
        overall_winner = "A" if comparison['scenario_a']['health_score'] > comparison['scenario_b']['health_score'] else "B"
        
        if comparison['scenario_a']['health_score'] == comparison['scenario_b']['health_score']:
            st.info("🤝 **Both scenarios show similar performance**")
        else:
            st.success(f"🏆 **Scenario {overall_winner}** shows better overall economic performance")
        
        # Detailed analysis
        with st.expander("🔍 Detailed Analysis"):
            st.write("**Key Differences:**")
            
            for metric, winner in zip(comparison_data['Metric'], comparison['winners']):
                if winner not in ['Tie', '🤝']:
                    st.write(f"• {metric}: **Scenario {winner}** performs better")

def create_parameter_inputs(suffix: str, label: str) -> Dict[str, Any]:
    """Create parameter input widgets with unique keys"""
    
    st.write(f"**{label}**")
    
    # Default values (different for A and B)
    defaults_a = {
        'creator_share': 0.40,
        'commission_share': 0.10,
        'burn_rate': 0.50,
        'quality_mult': 20.0,
        'daily_revenue': 50000,
        'daily_users': 100000
    }
    
    defaults_b = {
        'creator_share': 0.45,
        'commission_share': 0.08,
        'burn_rate': 0.70,
        'quality_mult': 25.0,
        'daily_revenue': 75000,
        'daily_users': 150000
    }
    
    defaults = defaults_a if suffix == 'a' else defaults_b
    
    return {
        'creator_share': st.slider(
            "Creator Share", 0.20, 0.60, defaults['creator_share'], 0.05, key=f"creator_{suffix}"
        ),
        'commission_share': st.slider(
            "Commission Share", 0.05, 0.20, defaults['commission_share'], 0.01, key=f"commission_{suffix}"
        ),
        'commission_burn_rate': st.slider(
            "Commission Burn Rate", 0.1, 1.0, defaults['burn_rate'], 0.1, key=f"burn_{suffix}"
        ),
        'max_quality_multiplier': st.slider(
            "Max Quality Multiplier", 5.0, 30.0, defaults['quality_mult'], 1.0, key=f"quality_{suffix}"
        ),
        'daily_revenue': st.number_input(
            "Daily Revenue ($)", 10000, 500000, defaults['daily_revenue'], 5000, key=f"revenue_{suffix}"
        ),
        'daily_users': st.number_input(
            "Daily Users", 10000, 1000000, defaults['daily_users'], 10000, key=f"users_{suffix}"
        )
    }

def run_quick_simulation(params: Dict[str, Any], days: int = 90) -> Dict[str, Any]:
    """Run quick simulation for A/B testing"""
    
    # Initialize engine
    engine_params = {
        'creator_share': params['creator_share'],
        'commission_share': params['commission_share'],
        'commission_burn_rate': params['commission_burn_rate'],
        'max_quality_multiplier': params['max_quality_multiplier'],
        'daily_revenue': params['daily_revenue'],
        'daily_users': params['daily_users'],
        'initial_price': 0.10
    }
    
    engine = VCoinEconomicEngine(engine_params)
    
    # Run simulation
    scenario_params = {
        'max_users': params['daily_users'] * 10,
        'growth_rate': 0.008,
        'base_daily_revenue': params['daily_revenue'],
        'content_creation_rate': 0.05
    }
    
    results = engine.run_simulation(scenario_params, days)
    
    # Calculate summary metrics
    df = pd.DataFrame(results)
    
    return {
        'final_price': df['current_price'].iloc[-1],
        'initial_price': df['current_price'].iloc[0],
        'price_appreciation': (df['current_price'].iloc[-1] / df['current_price'].iloc[0]) - 1,
        'supply_growth': (df['total_supply'].iloc[-1] / df['total_supply'].iloc[0]) - 1,
        'avg_creator_earnings': df['daily_rewards'].mean() * params['creator_share'],
        'platform_revenue': df['daily_rewards'].sum() * params['commission_share'],
        'health_score': calculate_economic_health_score(df),
        'avg_inflation': df['inflation_rate'].mean(),
        'avg_velocity': df['token_velocity'].mean()
    }

def compare_simulation_results(results_a: Dict[str, Any], results_b: Dict[str, Any]) -> Dict[str, Any]:
    """Compare results from two simulation scenarios"""
    
    # Determine winners for each metric
    winners = []
    
    metrics_higher_better = ['final_price', 'price_appreciation', 'avg_creator_earnings', 'platform_revenue', 'health_score']
    metrics_lower_better = ['supply_growth', 'avg_inflation']
    
    comparison_metrics = [
        'final_price', 'price_appreciation', 'supply_growth', 
        'avg_creator_earnings', 'platform_revenue', 'health_score'
    ]
    
    for metric in comparison_metrics:
        val_a = results_a[metric]
        val_b = results_b[metric]
        
        if abs(val_a - val_b) < 0.001:  # Essentially equal
            winners.append('🤝')
        elif metric in metrics_higher_better:
            winners.append('A' if val_a > val_b else 'B')
        elif metric in metrics_lower_better:
            winners.append('A' if val_a < val_b else 'B')
        else:
            winners.append('🤝')
    
    return {
        'scenario_a': results_a,
        'scenario_b': results_b,
        'winners': winners
    }

def calculate_economic_health_score(df: pd.DataFrame) -> float:
    """Calculate overall economic health score (0-100)"""
    
    # Price stability (25 points)
    price_volatility = df['current_price'].std() / df['current_price'].mean()
    price_score = max(0, 25 - (price_volatility * 100))
    
    # Supply management (25 points)
    avg_inflation = df['inflation_rate'].mean()
    supply_score = max(0, 25 - abs(avg_inflation - 0.10) * 250)  # Target 10% inflation
    
    # Token velocity (25 points)
    avg_velocity = df['token_velocity'].mean()
    velocity_score = max(0, 25 - abs(avg_velocity - 2.5) * 10)  # Target 2.5 velocity
    
    # Burn efficiency (25 points)
    burn_efficiency = df['daily_burns'].sum() / df['daily_rewards'].sum()
    efficiency_score = min(25, burn_efficiency * 50)
    
    total_score = price_score + supply_score + velocity_score + efficiency_score
    
    return min(100, max(0, total_score))

def display_detailed_breakdown(df: pd.DataFrame, params: Dict[str, Any]):
    """Display detailed economic breakdown"""
    
    st.subheader("📋 Economic Summary")
    
    # Calculate key statistics
    total_rewards_distributed = df['daily_rewards'].sum()
    total_burns_executed = df['daily_burns'].sum()
    net_token_change = total_rewards_distributed - total_burns_executed
    
    summary_data = {
        'Metric': [
            'Total Rewards Distributed',
            'Total Tokens Burned', 
            'Net Token Supply Change',
            'Average Daily Inflation',
            'Final Token Velocity',
            'Creator Total Earnings',
            'Platform Total Commission',
            'Economic Health Score'
        ],
        'Value': [
            f"{total_rewards_distributed:,.0f} VCOIN",
            f"{total_burns_executed:,.0f} VCOIN",
            f"{net_token_change:,.0f} VCOIN",
            f"{df['inflation_rate'].mean():.2%}",
            f"{df['token_velocity'].iloc[-1]:.2f}",
            f"{total_rewards_distributed * params['creator_share']:,.0f} VCOIN",
            f"{total_rewards_distributed * params['commission_share']:,.0f} VCOIN",
            f"{calculate_economic_health_score(df):.0f}/100"
        ],
        'USD Equivalent': [
            f"${total_rewards_distributed * df['current_price'].mean():,.0f}",
            f"${total_burns_executed * df['current_price'].mean():,.0f}",
            f"${net_token_change * df['current_price'].mean():,.0f}",
            "-",
            "-",
            f"${total_rewards_distributed * params['creator_share'] * df['current_price'].mean():,.0f}",
            f"${total_rewards_distributed * params['commission_share'] * df['current_price'].mean():,.0f}",
            "-"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

def export_simulation_data(df: pd.DataFrame, params: Dict[str, Any]):
    """Export simulation data for external analysis"""
    
    # Prepare export data
    export_data = {
        'simulation_metadata': {
            'timestamp': datetime.now().isoformat(),
            'parameters': params,
            'simulation_days': len(df),
            'final_metrics': {
                'final_price': df['current_price'].iloc[-1],
                'final_supply': df['total_supply'].iloc[-1],
                'total_rewards': df['daily_rewards'].sum(),
                'total_burns': df['daily_burns'].sum()
            }
        },
        'daily_data': df.to_dict('records')
    }
    
    # Convert to JSON
    json_data = json.dumps(export_data, indent=2)
    
    # Download button
    st.download_button(
        label="📁 Download Simulation Data (JSON)",
        data=json_data,
        file_name=f"vcoin_simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
    
    # CSV download
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📊 Download CSV Data",
        data=csv_data,
        file_name=f"vcoin_simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    st.success("📥 Simulation data ready for download!")

def get_method_rationale(method: str) -> str:
    """Get rationale for each valuation method"""
    
    rationales = {
        'revenue_multiple': 'Based on Web3 platform revenue multiples (15x)',
        'utility_value': 'Required token velocity for platform operations',
        'comparable_analysis': 'Similar Web3 social platform token prices',
        'cost_basis': 'Development and operational cost recovery',
        'network_value': 'Metcalfe\'s Law network effect valuation'
    }
    
    return rationales.get(method, 'Standard valuation method')

# Sidebar information
def display_sidebar_info():
    """Display helpful information in sidebar"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About This Playground")
    
    st.sidebar.markdown("""
    **This playground helps you:**
    - Test different tokenomics parameters
    - Calculate initial token price
    - Simulate economic scenarios
    - Compare parameter configurations
    - Export data for analysis
    
    **Key Features:**
    - Real-time parameter adjustment
    - Multi-method price discovery
    - Quality-based reward distribution
    - Economic health monitoring
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💡 Tips:**")
    st.sidebar.markdown("""
    - Higher burn rates = deflationary pressure
    - Quality multipliers reward better content
    - Accuracy bonuses incentivize truthful content
    - Monitor economic health score (aim for >70)
    """)

if __name__ == "__main__":
    # Initialize session state
    if 'simulation_run' not in st.session_state:
        st.session_state.simulation_run = False
    
    # Display sidebar info
    display_sidebar_info()
    
    # Run main interface
    main()
