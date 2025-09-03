#!/usr/bin/env python3
"""
Content Calculator vs VCOIN 4.0 Tokenomics Analysis
Run 10 scenarios to compare and optimize the tokenomics
"""

import math
import pandas as pd
from datetime import datetime

class ContentCalculatorEngine:
    """Simulate the Content Calculator logic"""
    
    def __init__(self):
        self.base_value_per_interaction = 0.005
        
    def calculate_scenario(self, scenario_params):
        """Calculate rewards using Content Calculator logic"""
        
        # Extract parameters
        daily_users = scenario_params['daily_users']
        daily_revenue = scenario_params['daily_revenue']
        revenue_share_percent = scenario_params['revenue_share_percent']
        vcoin_price = scenario_params['vcoin_price']
        view_count = scenario_params['view_count']
        engagement_rate = scenario_params['engagement_rate']
        content_type_multiplier = scenario_params['content_type_multiplier']
        quality_multiplier = scenario_params['quality_multiplier']
        
        # Calculate base reward pool
        daily_reward_pool = daily_revenue * (revenue_share_percent / 100)
        base_pool_per_view = daily_reward_pool / (daily_users * 100)  # Assuming 100 avg views per user
        
        # Content Calculator formula
        view_multiplier = 1.0 + math.log10(max(1, view_count)) / 3.0
        engagement_multiplier = 1.0 + (engagement_rate * 2.0)  # V4 formula
        
        # Calculate base VCOIN reward
        base_vcoin = base_pool_per_view * view_count
        total_vcoin = base_vcoin * content_type_multiplier * quality_multiplier * view_multiplier * engagement_multiplier
        
        # Distribution (from Content Calculator)
        creator_reward = total_vcoin * 0.40  # 40% to creator
        share_reward = total_vcoin * 0.20    # 20% to sharers
        viewer_reward = total_vcoin * 0.075  # 7.5% to viewers
        reaction_reward = total_vcoin * 0.10  # 10% to reactions
        platform_fee = total_vcoin * 0.225   # 22.5% platform operations
        
        total_usd = total_vcoin * vcoin_price
        creator_usd = creator_reward * vcoin_price
        
        return {
            'total_vcoin': total_vcoin,
            'total_usd': total_usd,
            'creator_vcoin': creator_reward,
            'creator_usd': creator_usd,
            'engagement_multiplier': engagement_multiplier,
            'view_multiplier': view_multiplier,
            'distribution': {
                'creator': creator_reward,
                'sharers': share_reward,
                'viewers': viewer_reward,
                'reactions': reaction_reward,
                'platform': platform_fee
            }
        }

class VCOIN4TokenomicsEngine:
    """Simulate VCOIN 4.0 Dynamic Calculator logic"""
    
    def __init__(self):
        self.total_supply = 10_000_000_000
        self.target_inflation = 0.08
        self.base_value_per_interaction = 0.005
        
    def calculate_scenario(self, scenario_params):
        """Calculate rewards using VCOIN 4.0 logic"""
        
        # Extract parameters
        daily_users = scenario_params['daily_users']
        current_token_price = scenario_params['current_token_price']
        initial_token_price = scenario_params['initial_token_price']
        market_efficiency = scenario_params['market_efficiency']
        investment_conversion = scenario_params['investment_conversion']
        content_posts_per_day = scenario_params['content_posts_per_day']
        avg_engagement_per_post = scenario_params['avg_engagement_per_post']
        
        # Community value calculation
        total_daily_engagement = content_posts_per_day * avg_engagement_per_post
        daily_community_value = total_daily_engagement * self.base_value_per_interaction
        monthly_community_value = daily_community_value * 30
        
        # Investment attraction
        price_change_percent = (current_token_price / initial_token_price - 1) * 100
        if price_change_percent <= 0:
            investment_multiplier = 0.5
        elif price_change_percent <= 25:
            investment_multiplier = 0.8
        elif price_change_percent <= 50:
            investment_multiplier = 1.0
        else:
            investment_multiplier = min(1.3, 1.0 + (price_change_percent - 50) / 200)
        
        theoretical_investment = monthly_community_value * investment_multiplier
        actual_investment = theoretical_investment * market_efficiency * investment_conversion
        
        # VCOIN 4.0 distribution
        creator_share = actual_investment * 0.40  # 40% to creators
        consumer_share = actual_investment * 0.35  # 35% to consumers
        platform_operations = actual_investment * 0.15  # 15% platform
        ecosystem_growth = actual_investment * 0.10  # 10% ecosystem
        
        # Calculate per creator
        creator_percentage = 0.01  # 1% of users are creators
        active_creators = int(daily_users * creator_percentage)
        avg_creator_reward_usd = creator_share / max(1, active_creators)
        
        # Dynamic reward adjustment
        price_appreciation_factor = current_token_price / initial_token_price
        reward_multiplier = 1.0 / (price_appreciation_factor ** 0.5)
        reward_multiplier = max(0.1, min(1.0, reward_multiplier))
        
        # Creator token rewards
        creator_token_value = avg_creator_reward_usd * 0.3  # 30% in tokens
        creator_token_amount = (creator_token_value / current_token_price) * reward_multiplier
        
        return {
            'monthly_community_value': monthly_community_value,
            'actual_investment': actual_investment,
            'creator_share': creator_share,
            'consumer_share': consumer_share,
            'platform_operations': platform_operations,
            'ecosystem_growth': ecosystem_growth,
            'avg_creator_reward_usd': avg_creator_reward_usd,
            'creator_token_amount': creator_token_amount,
            'reward_multiplier': reward_multiplier,
            'active_creators': active_creators,
            'price_appreciation': price_change_percent
        }

def generate_scenarios():
    """Generate 10 diverse scenarios for comparison"""
    
    scenarios = [
        {
            'name': 'Small Platform Startup',
            'daily_users': 5000,
            'daily_revenue': 1000,
            'revenue_share_percent': 70,
            'vcoin_price': 0.01,
            'view_count': 1000,
            'engagement_rate': 0.03,
            'content_type_multiplier': 1.2,
            'quality_multiplier': 1.5,
            # V4 params
            'current_token_price': 0.025,
            'initial_token_price': 0.01,
            'market_efficiency': 0.4,
            'investment_conversion': 0.2,
            'content_posts_per_day': 200,
            'avg_engagement_per_post': 15
        },
        {
            'name': 'Growing Community Platform',
            'daily_users': 25000,
            'daily_revenue': 8000,
            'revenue_share_percent': 75,
            'vcoin_price': 0.10,
            'view_count': 5000,
            'engagement_rate': 0.05,
            'content_type_multiplier': 1.5,
            'quality_multiplier': 1.8,
            # V4 params
            'current_token_price': 0.25,
            'initial_token_price': 0.10,
            'market_efficiency': 0.5,
            'investment_conversion': 0.3,
            'content_posts_per_day': 1000,
            'avg_engagement_per_post': 25
        },
        {
            'name': 'Mid-Scale Social Platform',
            'daily_users': 100000,
            'daily_revenue': 50000,
            'revenue_share_percent': 70,
            'vcoin_price': 0.50,
            'view_count': 25000,
            'engagement_rate': 0.08,
            'content_type_multiplier': 1.3,
            'quality_multiplier': 2.0,
            # V4 params
            'current_token_price': 1.25,
            'initial_token_price': 0.50,
            'market_efficiency': 0.6,
            'investment_conversion': 0.4,
            'content_posts_per_day': 5000,
            'avg_engagement_per_post': 50
        },
        {
            'name': 'Large Content Platform',
            'daily_users': 500000,
            'daily_revenue': 300000,
            'revenue_share_percent': 65,
            'vcoin_price': 1.00,
            'view_count': 100000,
            'engagement_rate': 0.06,
            'content_type_multiplier': 1.4,
            'quality_multiplier': 1.6,
            # V4 params
            'current_token_price': 2.50,
            'initial_token_price': 1.00,
            'market_efficiency': 0.7,
            'investment_conversion': 0.5,
            'content_posts_per_day': 20000,
            'avg_engagement_per_post': 75
        },
        {
            'name': 'YouTube-Scale Platform',
            'daily_users': 2000000,
            'daily_revenue': 1500000,
            'revenue_share_percent': 60,
            'vcoin_price': 2.00,
            'view_count': 500000,
            'engagement_rate': 0.04,
            'content_type_multiplier': 1.2,
            'quality_multiplier': 1.4,
            # V4 params
            'current_token_price': 5.00,
            'initial_token_price': 2.00,
            'market_efficiency': 0.8,
            'investment_conversion': 0.6,
            'content_posts_per_day': 80000,
            'avg_engagement_per_post': 100
        },
        {
            'name': 'High Engagement Niche',
            'daily_users': 50000,
            'daily_revenue': 15000,
            'revenue_share_percent': 80,
            'vcoin_price': 0.25,
            'view_count': 8000,
            'engagement_rate': 0.15,
            'content_type_multiplier': 2.0,
            'quality_multiplier': 2.2,
            # V4 params
            'current_token_price': 0.75,
            'initial_token_price': 0.25,
            'market_efficiency': 0.5,
            'investment_conversion': 0.3,
            'content_posts_per_day': 2000,
            'avg_engagement_per_post': 120
        },
        {
            'name': 'Bootstrap Mode Platform',
            'daily_users': 15000,
            'daily_revenue': 0,  # No external revenue
            'revenue_share_percent': 0,
            'vcoin_price': 0.05,
            'view_count': 3000,
            'engagement_rate': 0.07,
            'content_type_multiplier': 1.0,
            'quality_multiplier': 1.3,
            # V4 params
            'current_token_price': 0.15,
            'initial_token_price': 0.05,
            'market_efficiency': 0.3,
            'investment_conversion': 0.2,
            'content_posts_per_day': 800,
            'avg_engagement_per_post': 30
        },
        {
            'name': 'Premium Content Platform',
            'daily_users': 75000,
            'daily_revenue': 100000,
            'revenue_share_percent': 85,
            'vcoin_price': 5.00,
            'view_count': 15000,
            'engagement_rate': 0.12,
            'content_type_multiplier': 1.8,
            'quality_multiplier': 2.5,
            # V4 params
            'current_token_price': 12.50,
            'initial_token_price': 5.00,
            'market_efficiency': 0.6,
            'investment_conversion': 0.4,
            'content_posts_per_day': 3000,
            'avg_engagement_per_post': 180
        },
        {
            'name': 'Viral Content Platform',
            'daily_users': 300000,
            'daily_revenue': 75000,
            'revenue_share_percent': 70,
            'vcoin_price': 0.75,
            'view_count': 1000000,
            'engagement_rate': 0.02,
            'content_type_multiplier': 1.1,
            'quality_multiplier': 1.2,
            # V4 params
            'current_token_price': 1.50,
            'initial_token_price': 0.75,
            'market_efficiency': 0.7,
            'investment_conversion': 0.5,
            'content_posts_per_day': 15000,
            'avg_engagement_per_post': 200
        },
        {
            'name': 'Mature Ecosystem',
            'daily_users': 1000000,
            'daily_revenue': 500000,
            'revenue_share_percent': 65,
            'vcoin_price': 3.00,
            'view_count': 50000,
            'engagement_rate': 0.05,
            'content_type_multiplier': 1.3,
            'quality_multiplier': 1.7,
            # V4 params
            'current_token_price': 7.50,
            'initial_token_price': 3.00,
            'market_efficiency': 0.8,
            'investment_conversion': 0.6,
            'content_posts_per_day': 40000,
            'avg_engagement_per_post': 125
        }
    ]
    
    return scenarios

def analyze_scenarios():
    """Run all scenarios and compare Content Calculator vs VCOIN 4.0"""
    
    content_engine = ContentCalculatorEngine()
    v4_engine = VCOIN4TokenomicsEngine()
    
    scenarios = generate_scenarios()
    results = []
    
    print("🔍 Running 10 Content Calculator vs VCOIN 4.0 Scenarios...")
    print("=" * 80)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📊 Scenario {i}: {scenario['name']}")
        print("-" * 50)
        
        # Run Content Calculator
        content_result = content_engine.calculate_scenario(scenario)
        
        # Run VCOIN 4.0
        v4_result = v4_engine.calculate_scenario(scenario)
        
        # Compare results
        comparison = {
            'scenario_name': scenario['name'],
            'daily_users': scenario['daily_users'],
            'content_calc_creator_usd': content_result['creator_usd'],
            'content_calc_total_usd': content_result['total_usd'],
            'content_calc_creator_vcoin': content_result['creator_vcoin'],
            'v4_creator_monthly_usd': v4_result['avg_creator_reward_usd'],
            'v4_monthly_investment': v4_result['actual_investment'],
            'v4_creator_share': v4_result['creator_share'],
            'v4_active_creators': v4_result['active_creators'],
            'v4_price_appreciation': v4_result['price_appreciation'],
            'engagement_multiplier': content_result['engagement_multiplier'],
            'reward_multiplier': v4_result['reward_multiplier']
        }
        
        # Calculate daily equivalent for V4
        v4_daily_creator_usd = v4_result['avg_creator_reward_usd'] / 30
        
        # Display comparison
        print(f"Content Calculator (per content):")
        print(f"  • Creator Reward: ${content_result['creator_usd']:.2f} USD")
        print(f"  • Creator Tokens: {content_result['creator_vcoin']:.0f} VCOIN")
        print(f"  • Engagement Multiplier: {content_result['engagement_multiplier']:.2f}x")
        
        print(f"\nVCOIN 4.0 (monthly per creator):")
        print(f"  • Creator Reward: ${v4_result['avg_creator_reward_usd']:.2f} USD/month")
        print(f"  • Daily Equivalent: ${v4_daily_creator_usd:.2f} USD/day")
        print(f"  • Active Creators: {v4_result['active_creators']:,}")
        print(f"  • Price Appreciation: {v4_result['price_appreciation']:.1f}%")
        print(f"  • Reward Multiplier: {v4_result['reward_multiplier']:.3f}")
        
        # Calculate ratio
        if content_result['creator_usd'] > 0:
            ratio = v4_daily_creator_usd / content_result['creator_usd']
            print(f"\n💡 V4 vs Content Calc Ratio: {ratio:.2f}x")
            comparison['v4_vs_content_ratio'] = ratio
            
            if ratio > 1.5:
                print("   ⚠️  V4 pays significantly more")
            elif ratio < 0.5:
                print("   ⚠️  V4 pays significantly less")
            else:
                print("   ✅ V4 and Content Calculator are balanced")
        
        results.append(comparison)
    
    return results

def generate_optimization_recommendations(results):
    """Analyze results and provide optimization recommendations"""
    
    df = pd.DataFrame(results)
    
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE ANALYSIS & OPTIMIZATION RECOMMENDATIONS")
    print("=" * 80)
    
    # Calculate key statistics
    avg_ratio = df['v4_vs_content_ratio'].mean()
    median_ratio = df['v4_vs_content_ratio'].median()
    min_ratio = df['v4_vs_content_ratio'].min()
    max_ratio = df['v4_vs_content_ratio'].max()
    
    print(f"\n🎯 KEY METRICS:")
    print(f"  • Average V4/Content Ratio: {avg_ratio:.2f}x")
    print(f"  • Median Ratio: {median_ratio:.2f}x")
    print(f"  • Min Ratio: {min_ratio:.2f}x (Scenario: {df.loc[df['v4_vs_content_ratio'].idxmin(), 'scenario_name']})")
    print(f"  • Max Ratio: {max_ratio:.2f}x (Scenario: {df.loc[df['v4_vs_content_ratio'].idxmax(), 'scenario_name']})")
    
    # Identify imbalanced scenarios
    high_v4_scenarios = df[df['v4_vs_content_ratio'] > 1.5]
    low_v4_scenarios = df[df['v4_vs_content_ratio'] < 0.5]
    balanced_scenarios = df[(df['v4_vs_content_ratio'] >= 0.5) & (df['v4_vs_content_ratio'] <= 1.5)]
    
    print(f"\n📈 SCENARIO CLASSIFICATION:")
    print(f"  • V4 Overpaying (>1.5x): {len(high_v4_scenarios)} scenarios")
    print(f"  • V4 Underpaying (<0.5x): {len(low_v4_scenarios)} scenarios")
    print(f"  • Balanced (0.5x-1.5x): {len(balanced_scenarios)} scenarios")
    
    # Optimization recommendations
    print(f"\n🔧 OPTIMIZATION RECOMMENDATIONS:")
    
    if avg_ratio > 1.3:
        print(f"  ⚠️  V4 generally overpays compared to Content Calculator")
        print(f"     • Consider reducing creator share from 40% to 30-35%")
        print(f"     • Increase platform operations share to 20-25%")
        print(f"     • Adjust community value factor from $0.005 to $0.003-0.004")
    elif avg_ratio < 0.7:
        print(f"  ⚠️  V4 generally underpays compared to Content Calculator")
        print(f"     • Consider increasing creator share from 40% to 45-50%")
        print(f"     • Improve investment conversion rates")
        print(f"     • Increase community value factor to $0.006-0.008")
    else:
        print(f"  ✅ V4 is generally well-balanced with Content Calculator")
        print(f"     • Fine-tune individual parameters for edge cases")
    
    # Specific adjustments for imbalanced scenarios
    if len(high_v4_scenarios) > 0:
        print(f"\n⚡ HIGH V4 SCENARIOS NEED ADJUSTMENT:")
        for _, scenario in high_v4_scenarios.iterrows():
            print(f"  • {scenario['scenario_name']}: {scenario['v4_vs_content_ratio']:.2f}x ratio")
            
    if len(low_v4_scenarios) > 0:
        print(f"\n🚨 LOW V4 SCENARIOS NEED BOOST:")
        for _, scenario in low_v4_scenarios.iterrows():
            print(f"  • {scenario['scenario_name']}: {scenario['v4_vs_content_ratio']:.2f}x ratio")
    
    # Parameter correlation analysis
    print(f"\n🔬 PARAMETER CORRELATION INSIGHTS:")
    
    # Analyze engagement vs rewards
    high_engagement = df[df['engagement_multiplier'] > 1.15]
    low_engagement = df[df['engagement_multiplier'] <= 1.15]
    
    if len(high_engagement) > 0 and len(low_engagement) > 0:
        high_eng_ratio = high_engagement['v4_vs_content_ratio'].mean()
        low_eng_ratio = low_engagement['v4_vs_content_ratio'].mean()
        print(f"  • High Engagement Scenarios (>1.15x): Avg ratio {high_eng_ratio:.2f}x")
        print(f"  • Low Engagement Scenarios (≤1.15x): Avg ratio {low_eng_ratio:.2f}x")
        
        if high_eng_ratio > low_eng_ratio * 1.2:
            print(f"    → V4 favors high-engagement content more than Content Calculator")
        elif low_eng_ratio > high_eng_ratio * 1.2:
            print(f"    → Content Calculator favors high-engagement content more than V4")
    
    # Platform size analysis
    large_platforms = df[df['daily_users'] > 100000]
    small_platforms = df[df['daily_users'] <= 100000]
    
    if len(large_platforms) > 0 and len(small_platforms) > 0:
        large_ratio = large_platforms['v4_vs_content_ratio'].mean()
        small_ratio = small_platforms['v4_vs_content_ratio'].mean()
        print(f"  • Large Platforms (>100K users): Avg ratio {large_ratio:.2f}x")
        print(f"  • Small Platforms (≤100K users): Avg ratio {small_ratio:.2f}x")
        
        if large_ratio > small_ratio * 1.2:
            print(f"    → V4 favors larger platforms")
        elif small_ratio > large_ratio * 1.2:
            print(f"    → V4 favors smaller platforms")
    
    return df

def export_results(df):
    """Export detailed results to CSV"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"content_calc_vs_v4_analysis_{timestamp}.csv"
    
    df.to_csv(filename, index=False)
    print(f"\n💾 Results exported to: {filename}")
    
    # Create summary file
    summary_filename = f"tokenomics_optimization_summary_{timestamp}.txt"
    
    summary = f"""
VCOIN Content Calculator vs V4.0 Tokenomics Analysis
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY:
- Analyzed {len(df)} diverse platform scenarios
- Average V4/Content ratio: {df['v4_vs_content_ratio'].mean():.2f}x
- Median ratio: {df['v4_vs_content_ratio'].median():.2f}x
- Range: {df['v4_vs_content_ratio'].min():.2f}x to {df['v4_vs_content_ratio'].max():.2f}x

BALANCE ASSESSMENT:
- Balanced scenarios (0.5x-1.5x): {len(df[(df['v4_vs_content_ratio'] >= 0.5) & (df['v4_vs_content_ratio'] <= 1.5)])} out of {len(df)}
- V4 overpaying scenarios (>1.5x): {len(df[df['v4_vs_content_ratio'] > 1.5])}
- V4 underpaying scenarios (<0.5x): {len(df[df['v4_vs_content_ratio'] < 0.5])}

TOP SCENARIOS BY RATIO:
{df.nlargest(3, 'v4_vs_content_ratio')[['scenario_name', 'v4_vs_content_ratio']].to_string(index=False)}

BOTTOM SCENARIOS BY RATIO:
{df.nsmallest(3, 'v4_vs_content_ratio')[['scenario_name', 'v4_vs_content_ratio']].to_string(index=False)}

OPTIMIZATION RECOMMENDATIONS:
1. Adjust creator share percentage based on average ratio
2. Fine-tune community value factor for platform size
3. Optimize engagement multiplier coefficients
4. Balance investment conversion rates for different stages

See full CSV file for detailed data: {filename.replace(timestamp, '*')}
"""
    
    with open(summary_filename, 'w') as f:
        f.write(summary)
    
    print(f"📋 Summary exported to: {summary_filename}")

def main():
    """Main analysis function"""
    
    print("🚀 VCOIN Content Calculator vs V4.0 Tokenomics Analysis")
    print("🎯 Analyzing 10 scenarios to optimize tokenomics alignment")
    print("=" * 80)
    
    # Run scenario analysis
    results = analyze_scenarios()
    
    # Generate optimization recommendations
    df = generate_optimization_recommendations(results)
    
    # Export results
    export_results(df)
    
    print(f"\n✅ Analysis complete! Check the exported files for detailed results.")
    print(f"🔧 Use these insights to refine the Creator-Consumer Balance Calculator.")

if __name__ == "__main__":
    main()
