#!/usr/bin/env python3
"""
VCOIN 4.0: REALISTIC ECONOMIC MODEL
Balanced assumptions based on stress test findings for genuine sustainability
"""

import math
import pandas as pd

def realistic_community_economics(scenario_params):
    """Realistic economic modeling with validated assumptions"""
    
    # Extract parameters
    daily_users = scenario_params['daily_users']
    creator_percentage = scenario_params.get('creator_percentage', 2.5)
    content_per_creator = scenario_params.get('content_per_creator', 1.8)
    base_token_price = scenario_params.get('base_token_price', 0.10)
    current_token_price = scenario_params.get('current_token_price', 0.135)
    target_rpm = scenario_params.get('target_rpm', 3.0)
    
    # REALISTIC ASSUMPTIONS (Based on stress test learnings)
    community_value_factor = scenario_params.get('community_value_factor', 0.8)  # Moderate
    market_efficiency = scenario_params.get('market_efficiency', 0.6)  # 60% conversion
    investment_conversion_rate = scenario_params.get('investment_conversion_rate', 0.4)  # 40% actually invest
    market_sentiment = scenario_params.get('market_sentiment', 0.8)  # Slightly bearish default
    competition_factor = scenario_params.get('competition_factor', 0.75)  # Some competition
    
    # Calculate derived metrics
    daily_creators = int(daily_users * creator_percentage / 100)
    daily_content = int(daily_creators * content_per_creator)
    
    # REALISTIC community value creation
    # Base value: $0.005 per meaningful interaction (5x more than ultra-conservative)
    base_value_per_interaction = 0.005
    
    # Engagement rates: Not everyone interacts with every content
    engagement_rate = min(0.3, math.log(daily_users + 1) / math.log(100000 + 1))  # 10-30% engagement
    daily_meaningful_interactions = daily_users * daily_content * engagement_rate
    
    base_community_value = (daily_meaningful_interactions * 
                           base_value_per_interaction * 
                           community_value_factor)
    
    # Apply market conditions
    adjusted_community_value = (base_community_value * 
                               market_efficiency * 
                               market_sentiment * 
                               competition_factor)
    
    monthly_community_value = adjusted_community_value * 30
    
    # REALISTIC investment model
    price_appreciation = max(0, (current_token_price / base_token_price - 1) * 100)
    
    # Investment interest based on price appreciation and market conditions
    if price_appreciation <= 0:
        base_investment_interest = 0.3  # Some speculative interest
    elif price_appreciation <= 25:
        base_investment_interest = 0.7  # Moderate interest
    elif price_appreciation <= 50:
        base_investment_interest = 1.0  # Strong interest
    elif price_appreciation <= 100:
        base_investment_interest = 1.2  # High interest
    else:
        base_investment_interest = min(1.5, 1.0 + (price_appreciation - 100) / 300)  # Diminishing returns
    
    # Apply investment conversion rate
    theoretical_investment_interest = monthly_community_value * base_investment_interest
    actual_investment_inflow = theoretical_investment_interest * investment_conversion_rate
    
    # Creator economics
    avg_monthly_views = 22000  # Realistic estimate
    target_monthly_earnings = (avg_monthly_views / 1000) * target_rpm
    total_creator_target_usd = daily_creators * target_monthly_earnings
    
    # Investment allocation (realistic)
    investment_to_creators = actual_investment_inflow * 0.7  # 70% to creators
    investment_to_platform = actual_investment_inflow * 0.2  # 20% to platform
    investment_to_reserves = actual_investment_inflow * 0.1  # 10% to reserves
    
    investment_surplus = investment_to_creators - total_creator_target_usd
    
    # Token inflation calculation (if needed)
    if investment_surplus >= 0:
        token_inflation_needed_usd = 0
        coverage_ratio = investment_to_creators / max(1, total_creator_target_usd)
    else:
        remaining_need = abs(investment_surplus)
        
        # Dynamic reward adjustment
        if current_token_price <= base_token_price:
            reward_multiplier = 1.0
        else:
            price_appreciation_ratio = current_token_price / base_token_price
            raw_multiplier = 1.0 / (price_appreciation_ratio ** 0.3)
            reward_multiplier = max(0.2, min(2.0, raw_multiplier))
        
        tokens_needed = remaining_need / current_token_price
        adjusted_tokens = tokens_needed * reward_multiplier
        token_inflation_needed_usd = adjusted_tokens * current_token_price
        coverage_ratio = investment_to_creators / max(1, total_creator_target_usd)
    
    # Calculate total platform costs
    total_platform_costs = total_creator_target_usd + token_inflation_needed_usd
    
    # Economic health (realistic scoring)
    annual_inflation_rate = (token_inflation_needed_usd * 12) / (1_000_000_000 * current_token_price) * 100
    
    inflation_score = 90 if annual_inflation_rate <= 5 else max(0, 90 - (annual_inflation_rate - 5) * 8)
    creator_score = min(100, (target_rpm / 3.0) * 100)
    sustainability_score = min(100, max(0, (coverage_ratio - 0.5) * 100))  # Penalize low coverage
    market_score = min(100, market_sentiment * 100)
    
    economic_health = (inflation_score + creator_score + sustainability_score + market_score) / 4
    
    return {
        'scenario_name': scenario_params['name'],
        'daily_users': daily_users,
        'daily_creators': daily_creators,
        'engagement_rate': engagement_rate,
        'monthly_community_value': monthly_community_value,
        'theoretical_investment_interest': theoretical_investment_interest,
        'actual_investment_inflow': actual_investment_inflow,
        'investment_to_creators': investment_to_creators,
        'total_creator_target_usd': total_creator_target_usd,
        'investment_surplus': investment_surplus,
        'coverage_ratio': coverage_ratio,
        'token_inflation_needed_usd': token_inflation_needed_usd,
        'annual_inflation_rate': annual_inflation_rate,
        'economic_health': economic_health,
        'total_platform_costs': total_platform_costs,
        'equivalent_arpu': actual_investment_inflow / daily_users if daily_users > 0 else 0
    }

def run_realistic_analysis():
    """Run realistic 20-scenario analysis"""
    
    print("🎯 VCOIN 4.0: REALISTIC ECONOMIC MODEL VALIDATION")
    print("=" * 80)
    print("Balanced assumptions based on stress test insights")
    print()
    
    print("📊 REALISTIC ASSUMPTIONS:")
    print("   • Community value factor: 0.8 (moderate)")
    print("   • Market efficiency: 60% (reasonable conversion)")
    print("   • Investment conversion: 40% (realistic investor behavior)")
    print("   • Market sentiment: 80% (slightly bearish)")
    print("   • Competition factor: 75% (moderate competition)")
    print("   • Value per interaction: $0.005 (validated estimate)")
    print()
    
    scenarios = [
        # Normal scenarios
        {'name': '🌱 Launch Phase', 'daily_users': 3000, 'market_sentiment': 1.0},
        {'name': '📈 Early Growth', 'daily_users': 8000, 'market_sentiment': 1.1},
        {'name': '🚀 Growth Phase', 'daily_users': 15000, 'market_sentiment': 1.0},
        {'name': '🏢 Scale Phase', 'daily_users': 25000, 'market_sentiment': 0.9},
        {'name': '🌍 Major Platform', 'daily_users': 50000, 'market_sentiment': 0.8},
        
        # Market condition scenarios
        {'name': '💥 Bear Market', 'daily_users': 20000, 'market_sentiment': 0.4, 'current_token_price': 0.08},
        {'name': '📉 Market Correction', 'daily_users': 15000, 'market_sentiment': 0.6, 'current_token_price': 0.09},
        {'name': '🔴 Recession', 'daily_users': 12000, 'market_sentiment': 0.5, 'current_token_price': 0.07},
        {'name': '⚡ Flash Crash', 'daily_users': 18000, 'market_sentiment': 0.3, 'current_token_price': 0.05},
        {'name': '🌈 Bull Market', 'daily_users': 22000, 'market_sentiment': 1.3, 'current_token_price': 0.25},
        
        # Competition scenarios
        {'name': '⚔️ High Competition', 'daily_users': 30000, 'community_value_factor': 0.6, 'competition_factor': 0.5},
        {'name': '🎪 Fad Platform', 'daily_users': 35000, 'community_value_factor': 0.4, 'market_sentiment': 0.6},
        {'name': '🏁 Market Saturation', 'daily_users': 40000, 'community_value_factor': 0.7, 'competition_factor': 0.6},
        
        # Platform lifecycle scenarios
        {'name': '🎭 Mature Platform', 'daily_users': 45000, 'target_rpm': 4.0, 'creator_percentage': 3.5},
        {'name': '🔄 Platform Decline', 'daily_users': 20000, 'community_value_factor': 0.5, 'market_sentiment': 0.6},
        {'name': '📱 Mobile Shift', 'daily_users': 35000, 'community_value_factor': 0.7, 'content_per_creator': 1.2},
        {'name': '🤖 AI Impact', 'daily_users': 28000, 'community_value_factor': 0.6, 'content_per_creator': 2.5},
        
        # Stress scenarios
        {'name': '🌪️ Multiple Crises', 'daily_users': 10000, 'community_value_factor': 0.4, 'market_sentiment': 0.3, 'current_token_price': 0.06},
        {'name': '🌊 Liquidity Crisis', 'daily_users': 15000, 'investment_conversion_rate': 0.1, 'market_sentiment': 0.4},
        {'name': '⏰ Long-term Reality', 'daily_users': 60000, 'community_value_factor': 0.6, 'target_rpm': 4.5, 'creator_percentage': 4.0}
    ]
    
    results = []
    for scenario in scenarios:
        result = realistic_community_economics(scenario)
        results.append(result)
    
    # Analysis
    print("📊 REALISTIC MODEL RESULTS")
    print("=" * 80)
    
    print(f"{'Scenario':<22} {'Users':<8} {'Coverage':<9} {'Inflation':<9} {'Health':<7} {'ARPU':<8} {'Status':<10}")
    print("-" * 80)
    
    success_count = 0
    warning_count = 0
    failure_count = 0
    
    for result in results:
        scenario = result['scenario_name'][:21]
        users = f"{result['daily_users']:,}"
        coverage = f"{result['coverage_ratio']:.1f}x"
        inflation = f"{result['annual_inflation_rate']:.1f}%"
        health = f"{result['economic_health']:.0f}"
        arpu = f"${result['equivalent_arpu']:.0f}"
        
        if (result['coverage_ratio'] >= 0.8 and 
            result['annual_inflation_rate'] <= 8 and 
            result['economic_health'] >= 60):
            status = "✅ SUCCESS"
            success_count += 1
        elif (result['coverage_ratio'] >= 0.5 and 
              result['annual_inflation_rate'] <= 15 and 
              result['economic_health'] >= 45):
            status = "⚠️ WARNING"
            warning_count += 1
        else:
            status = "❌ FAILURE"
            failure_count += 1
        
        print(f"{scenario:<22} {users:<8} {coverage:<9} {inflation:<9} {health:<7} {arpu:<8} {status:<10}")
    
    success_rate = success_count / len(results) * 100
    
    print()
    print("🎯 REALISTIC MODEL ANALYSIS")
    print("=" * 80)
    print(f"Total Scenarios: {len(results)}")
    print(f"✅ Success: {success_count} ({success_rate:.0f}%)")
    print(f"⚠️ Warning: {warning_count} ({warning_count/len(results)*100:.0f}%)")
    print(f"❌ Failure: {failure_count} ({failure_count/len(results)*100:.0f}%)")
    
    # Detailed analysis
    if success_count > 0:
        successes = [r for r in results if (r['coverage_ratio'] >= 0.8 and 
                                           r['annual_inflation_rate'] <= 8 and 
                                           r['economic_health'] >= 60)]
        
        avg_coverage = sum(s['coverage_ratio'] for s in successes) / len(successes)
        avg_investment = sum(s['actual_investment_inflow'] for s in successes) / len(successes)
        avg_arpu = sum(s['equivalent_arpu'] for s in successes) / len(successes)
        
        print()
        print("📈 SUCCESS METRICS:")
        print(f"   • Average Coverage: {avg_coverage:.1f}x")
        print(f"   • Average Investment: ${avg_investment:,.0f}/month")
        print(f"   • Average Equivalent ARPU: ${avg_arpu:.2f}")
    
    if failure_count > 0:
        print()
        print("⚠️ FAILURE ANALYSIS:")
        failures = [r for r in results if not (r['coverage_ratio'] >= 0.5 and 
                                              r['annual_inflation_rate'] <= 15 and 
                                              r['economic_health'] >= 45)]
        
        for failure in failures[:3]:  # Show top 3 failures
            print(f"   • {failure['scenario_name']}: {failure['coverage_ratio']:.2f}x coverage, needs ${abs(failure['investment_surplus']):,.0f} token support")
    
    # Key insights
    print()
    print("💡 KEY INSIGHTS:")
    
    min_coverage = min(r['coverage_ratio'] for r in results)
    max_coverage = max(r['coverage_ratio'] for r in results)
    avg_coverage_all = sum(r['coverage_ratio'] for r in results) / len(results)
    
    print(f"   • Coverage Range: {min_coverage:.1f}x to {max_coverage:.1f}x")
    print(f"   • Average Coverage: {avg_coverage_all:.1f}x")
    
    if avg_coverage_all >= 1.0:
        print("   ✅ Model shows overall sustainability with realistic assumptions")
    elif avg_coverage_all >= 0.7:
        print("   ⚠️ Model needs optimization but shows potential")
    else:
        print("   ❌ Model requires fundamental changes")
    
    # Calculate required external funding
    total_shortfall = sum(abs(r['investment_surplus']) for r in results if r['investment_surplus'] < 0)
    scenarios_needing_support = len([r for r in results if r['investment_surplus'] < 0])
    
    if scenarios_needing_support > 0:
        avg_shortfall = total_shortfall / scenarios_needing_support
        print(f"   • Scenarios needing token support: {scenarios_needing_support}/{len(results)}")
        print(f"   • Average shortfall when needed: ${avg_shortfall:,.0f}")
    
    return results, success_rate

def calculate_minimum_viable_community():
    """Calculate minimum community size and engagement needed for sustainability"""
    
    print("\n" + "=" * 80)
    print("🎯 MINIMUM VIABLE COMMUNITY ANALYSIS")
    print("=" * 80)
    
    # Test minimum thresholds
    min_viable_configs = []
    
    for users in range(5000, 50001, 5000):  # Test 5K to 50K users
        for value_factor in [0.5, 0.7, 1.0, 1.3, 1.5]:
            scenario = {
                'name': f'{users:,} users, {value_factor}x factor',
                'daily_users': users,
                'community_value_factor': value_factor,
                'market_efficiency': 0.6,
                'investment_conversion_rate': 0.4,
                'market_sentiment': 0.8,
                'competition_factor': 0.75
            }
            
            result = realistic_community_economics(scenario)
            
            if result['coverage_ratio'] >= 1.0:  # Sustainable
                min_viable_configs.append((users, value_factor, result['coverage_ratio'], result['actual_investment_inflow']))
    
    if min_viable_configs:
        print("✅ MINIMUM VIABLE CONFIGURATIONS:")
        # Sort by users, then by value factor
        sorted_configs = sorted(min_viable_configs, key=lambda x: (x[0], x[1]))
        
        for users, factor, coverage, investment in sorted_configs[:8]:  # Show first 8
            print(f"   • {users:,} users with {factor}x community factor: {coverage:.1f}x coverage (${investment:,.0f} investment)")
        
        # Find absolute minimum
        min_config = min(sorted_configs, key=lambda x: (x[0], x[1]))
        print()
        print(f"🎯 ABSOLUTE MINIMUM VIABLE:")
        print(f"   • {min_config[0]:,} users with {min_config[1]}x community factor")
        print(f"   • Achieves {min_config[2]:.1f}x sustainability")
        print(f"   • Generates ${min_config[3]:,.0f} monthly investment")
        
    else:
        print("❌ NO VIABLE CONFIGURATIONS FOUND")
        print("   Model requires optimization for sustainability")
    
    return min_viable_configs

if __name__ == "__main__":
    # Run realistic analysis
    results, success_rate = run_realistic_analysis()
    
    # Find minimum viable community
    viable_configs = calculate_minimum_viable_community()
    
    print("\n" + "=" * 80)
    print("🏆 FINAL REALISTIC MODEL VERDICT")
    print("=" * 80)
    
    if success_rate >= 70:
        verdict = "🟢 VALIDATED - Ready for implementation"
    elif success_rate >= 50:
        verdict = "🟡 PROMISING - Needs parameter tuning"
    else:
        verdict = "🔴 CHALLENGING - Requires significant optimization"
    
    print(f"Success Rate: {success_rate:.0f}%")
    print(f"Verdict: {verdict}")
    
    if viable_configs:
        min_users = min(config[0] for config in viable_configs)
        min_factor = min(config[1] for config in viable_configs if config[0] == min_users)
        print(f"Minimum Viable: {min_users:,} users with {min_factor}x community factor")
    
    avg_coverage = sum(r['coverage_ratio'] for r in results) / len(results)
    print(f"Average Coverage: {avg_coverage:.1f}x")
    
    if avg_coverage >= 1.0:
        print("💡 Model shows realistic sustainability potential")
    else:
        print("💡 Model needs optimization for consistent sustainability")
    
    print("=" * 80)
