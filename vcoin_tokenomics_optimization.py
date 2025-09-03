#!/usr/bin/env python3
"""
VCOIN Tokenomics Optimization Based on Analysis
Apply adjustments to align V4.0 with Content Calculator
"""

import math

class OptimizedVCOINCalculator:
    """Optimized VCOIN calculator with balanced parameters"""
    
    def __init__(self):
        # Optimized parameters based on analysis
        self.total_supply = 10_000_000_000
        self.target_inflation = 0.08
        
        # CRITICAL ADJUSTMENTS from analysis:
        self.base_value_per_interaction = 0.025  # Increased from 0.005 to 0.025 (5x boost)
        
        # Optimized distribution (adjusted from analysis)
        self.creator_share = 0.55  # Increased from 40% to 55%
        self.consumer_share = 0.25  # Reduced from 35% to 25%
        self.platform_operations = 0.12  # Reduced from 15% to 12%
        self.ecosystem_growth = 0.08   # Reduced from 10% to 8%
        
        # Enhanced conversion rates
        self.min_market_efficiency = 0.6  # Increased from 0.3-0.9 range
        self.min_investment_conversion = 0.4  # Increased from 0.1-0.7 range
        
    def calculate_optimized_rewards(self, platform_params):
        """Calculate rewards with optimized parameters"""
        
        daily_users = platform_params['daily_users']
        current_token_price = platform_params['current_token_price']
        initial_token_price = platform_params['initial_token_price']
        content_posts_per_day = platform_params['content_posts_per_day']
        avg_engagement_per_post = platform_params['avg_engagement_per_post']
        market_efficiency = max(self.min_market_efficiency, platform_params.get('market_efficiency', 0.6))
        investment_conversion = max(self.min_investment_conversion, platform_params.get('investment_conversion', 0.4))
        
        # Enhanced community value calculation
        total_daily_engagement = content_posts_per_day * avg_engagement_per_post
        daily_community_value = total_daily_engagement * self.base_value_per_interaction
        monthly_community_value = daily_community_value * 30
        
        # Investment attraction (same formula, but better conversion rates)
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
        
        # Optimized distribution
        creator_share = actual_investment * self.creator_share
        consumer_share = actual_investment * self.consumer_share
        platform_operations = actual_investment * self.platform_operations
        ecosystem_growth = actual_investment * self.ecosystem_growth
        
        # Calculate per creator with enhanced parameters
        creator_percentage = 0.025  # Increased from 1% to 2.5% (more realistic)
        active_creators = int(daily_users * creator_percentage)
        avg_creator_reward_usd = creator_share / max(1, active_creators)
        
        # Enhanced dynamic reward adjustment
        price_appreciation_factor = current_token_price / initial_token_price
        reward_multiplier = 1.0 / (price_appreciation_factor ** 0.3)  # Reduced exponent from 0.5 to 0.3
        reward_multiplier = max(0.2, min(1.0, reward_multiplier))  # Increased minimum from 0.1 to 0.2
        
        return {
            'daily_community_value': daily_community_value,
            'monthly_community_value': monthly_community_value,
            'actual_investment': actual_investment,
            'creator_share': creator_share,
            'consumer_share': consumer_share,
            'platform_operations': platform_operations,
            'ecosystem_growth': ecosystem_growth,
            'avg_creator_reward_usd': avg_creator_reward_usd,
            'active_creators': active_creators,
            'reward_multiplier': reward_multiplier,
            'price_appreciation': price_change_percent,
            'optimization_boost': 'Enhanced 5x community value + 55% creator share + better conversions'
        }

def test_optimized_parameters():
    """Test the optimized parameters against original scenarios"""
    
    calculator = OptimizedVCOINCalculator()
    
    test_scenarios = [
        {
            'name': 'Small Platform Startup',
            'daily_users': 5000,
            'current_token_price': 0.025,
            'initial_token_price': 0.01,
            'content_posts_per_day': 200,
            'avg_engagement_per_post': 15,
            'market_efficiency': 0.6,  # Enhanced
            'investment_conversion': 0.4  # Enhanced
        },
        {
            'name': 'Growing Community Platform',
            'daily_users': 25000,
            'current_token_price': 0.25,
            'initial_token_price': 0.10,
            'content_posts_per_day': 1000,
            'avg_engagement_per_post': 25,
            'market_efficiency': 0.6,
            'investment_conversion': 0.4
        },
        {
            'name': 'Large Content Platform',
            'daily_users': 500000,
            'current_token_price': 2.50,
            'initial_token_price': 1.00,
            'content_posts_per_day': 20000,
            'avg_engagement_per_post': 75,
            'market_efficiency': 0.7,
            'investment_conversion': 0.5
        }
    ]
    
    print("🔧 Testing Optimized VCOIN Parameters")
    print("=" * 60)
    
    for scenario in test_scenarios:
        result = calculator.calculate_optimized_rewards(scenario)
        
        print(f"\n📊 {scenario['name']}")
        print(f"  • Community Value: ${result['monthly_community_value']:,.0f}/month")
        print(f"  • Investment Inflow: ${result['actual_investment']:,.0f}/month")
        print(f"  • Creator Share (55%): ${result['creator_share']:,.0f}/month")
        print(f"  • Active Creators: {result['active_creators']:,}")
        print(f"  • Avg Creator Reward: ${result['avg_creator_reward_usd']:,.0f}/month")
        print(f"  • Daily Equivalent: ${result['avg_creator_reward_usd']/30:,.0f}/day")
        print(f"  • Optimization: {result['optimization_boost']}")
    
    return calculator

if __name__ == "__main__":
    test_optimized_parameters()
