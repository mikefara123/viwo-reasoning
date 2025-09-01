#!/usr/bin/env python3
"""
VCOIN Command Line Tester
Quick testing interface for tokenomics without GUI
"""

import argparse
import json
import sys
from typing import Dict, Any
from vcoin_economic_engine import VCoinEconomicEngine, VCoinColdStartValuation, ContentMetrics

class VCoinCLI:
    """Command line interface for VCOIN economic testing"""
    
    def __init__(self):
        self.default_params = {
            'creator_share': 0.40,
            'engagement_share': 0.40,
            'commission_share': 0.10,
            'royalty_share': 0.10,
            'daily_revenue': 50000,
            'daily_users': 100000,
            'commission_burn_rate': 0.50,
            'max_quality_multiplier': 20.0,
            'initial_supply': 1_000_000_000
        }
    
    def test_content_reward(self, content_params: Dict[str, Any]) -> Dict[str, Any]:
        """Test reward calculation for specific content"""
        
        # Create content metrics
        content = ContentMetrics(
            content_type=content_params.get('type', 'short_video'),
            view_count=content_params.get('views', 1000),
            shares=content_params.get('shares', 30),
            reports=content_params.get('reports', 5),
            likes=content_params.get('likes', 150),
            dislikes=content_params.get('dislikes', 20),
            comments=content_params.get('comments', 50),
            creator_5a_score=content_params.get('creator_5a', 300),
            accuracy_rating=content_params.get('accuracy', 80),
            engagement_quality=content_params.get('engagement_quality', 70)
        )
        
        # Initialize engine
        engine = VCoinEconomicEngine(self.default_params)
        
        # Calculate rewards
        reward_result = engine.calculate_content_reward(content)
        
        return {
            'content_type': content.content_type,
            'total_reward_vcoin': reward_result['total_reward'],
            'total_reward_usd': reward_result['total_reward'] * 0.10,
            'creator_reward_vcoin': reward_result['creator_reward'],
            'creator_reward_usd': reward_result['creator_reward'] * 0.10,
            'platform_commission_vcoin': reward_result['platform_commission'],
            'platform_commission_usd': reward_result['platform_commission'] * 0.10,
            'engagement_breakdown': {
                'share_per_action': reward_result['share_per_action'],
                'like_per_action': reward_result['like_per_action'],
                'comment_per_action': reward_result['comment_per_action']
            }
        }
    
    def test_price_discovery(self, platform_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Test initial price discovery"""
        
        valuator = VCoinColdStartValuation()
        valuation_result = valuator.calculate_initial_price(platform_metrics)
        
        return {
            'recommended_price': valuation_result['recommended_price'],
            'confidence_range': valuation_result['confidence_range'],
            'method_breakdown': valuation_result['individual_valuations']
        }
    
    def test_economic_scenario(self, scenario_params: Dict[str, Any], days: int = 90) -> Dict[str, Any]:
        """Test complete economic scenario"""
        
        # Merge with defaults
        params = {**self.default_params, **scenario_params}
        
        # Initialize engine
        engine = VCoinEconomicEngine(params)
        
        # Run simulation
        sim_scenario = {
            'max_users': params['daily_users'] * 10,
            'growth_rate': 0.008,
            'base_daily_revenue': params['daily_revenue'],
            'content_creation_rate': 0.05
        }
        
        results = engine.run_simulation(sim_scenario, days)
        
        # Calculate summary
        if not results:
            return {'error': 'Simulation failed'}
        
        final_result = results[-1]
        initial_result = results[0]
        
        return {
            'simulation_days': days,
            'initial_price': initial_result['current_price'],
            'final_price': final_result['current_price'],
            'price_change': (final_result['current_price'] / initial_result['current_price']) - 1,
            'initial_supply': initial_result['total_supply'],
            'final_supply': final_result['total_supply'],
            'supply_change': (final_result['total_supply'] / initial_result['total_supply']) - 1,
            'total_rewards': sum(day['daily_rewards'] for day in results),
            'total_burns': sum(day['daily_burns'] for day in results),
            'avg_daily_creator_earnings': (sum(day['daily_rewards'] for day in results) * params['creator_share']) / days,
            'economic_health': self.calculate_health_score(results)
        }
    
    def calculate_health_score(self, results: list) -> float:
        """Calculate economic health score"""
        
        if not results:
            return 0
        
        # Extract metrics
        prices = [day['current_price'] for day in results]
        supplies = [day['total_supply'] for day in results]
        rewards = [day['daily_rewards'] for day in results]
        burns = [day['daily_burns'] for day in results]
        
        # Price stability
        price_volatility = (max(prices) - min(prices)) / ((max(prices) + min(prices)) / 2)
        price_score = max(0, 25 - (price_volatility * 100))
        
        # Supply management
        supply_growth = (supplies[-1] / supplies[0]) - 1
        supply_score = max(0, 25 - abs(supply_growth - 0.10) * 250)
        
        # Burn efficiency
        total_rewards = sum(rewards)
        total_burns = sum(burns)
        burn_efficiency = total_burns / total_rewards if total_rewards > 0 else 0
        burn_score = min(25, burn_efficiency * 50)
        
        # Activity growth
        activity_growth = len([r for r in rewards if r > 0]) / len(rewards)
        activity_score = activity_growth * 25
        
        return price_score + supply_score + burn_score + activity_score
    
    def run_comparison_test(self, params_a: Dict[str, Any], params_b: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two parameter configurations"""
        
        print("🔄 Running comparison test...")
        
        # Test both scenarios
        result_a = self.test_economic_scenario(params_a)
        result_b = self.test_economic_scenario(params_b)
        
        # Determine winners
        comparison = {
            'scenario_a': result_a,
            'scenario_b': result_b,
            'winners': {
                'price_performance': 'A' if result_a['price_change'] > result_b['price_change'] else 'B',
                'supply_management': 'A' if abs(result_a['supply_change'] - 0.1) < abs(result_b['supply_change'] - 0.1) else 'B',
                'creator_earnings': 'A' if result_a['avg_daily_creator_earnings'] > result_b['avg_daily_creator_earnings'] else 'B',
                'economic_health': 'A' if result_a['economic_health'] > result_b['economic_health'] else 'B'
            }
        }
        
        return comparison

def main():
    """Main CLI interface"""
    
    parser = argparse.ArgumentParser(description='VCOIN Economic Testing CLI')
    parser.add_argument('command', choices=['content', 'price', 'simulate', 'compare'], 
                       help='Command to run')
    parser.add_argument('--config', type=str, help='JSON config file path')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--days', type=int, default=90, help='Simulation days')
    
    # Content-specific arguments
    parser.add_argument('--type', type=str, default='short_video', 
                       choices=['podcast', 'long_video', 'short_video', 'text_post'])
    parser.add_argument('--views', type=int, default=1000)
    parser.add_argument('--shares', type=int, default=30)
    parser.add_argument('--likes', type=int, default=150)
    parser.add_argument('--comments', type=int, default=50)
    parser.add_argument('--creator-5a', type=int, default=300)
    parser.add_argument('--accuracy', type=int, default=80)
    
    # Economic parameters
    parser.add_argument('--daily-revenue', type=int, default=50000)
    parser.add_argument('--daily-users', type=int, default=100000)
    parser.add_argument('--creator-share', type=float, default=0.40)
    parser.add_argument('--burn-rate', type=float, default=0.50)
    
    args = parser.parse_args()
    
    cli = VCoinCLI()
    
    if args.command == 'content':
        # Test content reward calculation
        content_params = {
            'type': args.type,
            'views': args.views,
            'shares': args.shares,
            'likes': args.likes,
            'comments': args.comments,
            'creator_5a': args.creator_5a,
            'accuracy': args.accuracy
        }
        
        result = cli.test_content_reward(content_params)
        
        print("🎬 Content Reward Calculation:")
        print(f"  Content Type: {result['content_type']}")
        print(f"  Total Reward: {result['total_reward_vcoin']:,.0f} VCOIN (${result['total_reward_usd']:,.2f})")
        print(f"  Creator Reward: {result['creator_reward_vcoin']:,.0f} VCOIN (${result['creator_reward_usd']:,.2f})")
        print(f"  Platform Commission: {result['platform_commission_vcoin']:,.0f} VCOIN (${result['platform_commission_usd']:,.2f})")
        print(f"  Share Reward: {result['engagement_breakdown']['share_per_action']:,.3f} VCOIN per share")
        print(f"  Like Reward: {result['engagement_breakdown']['like_per_action']:,.3f} VCOIN per like")
        print(f"  Comment Reward: {result['engagement_breakdown']['comment_per_action']:,.3f} VCOIN per comment")
    
    elif args.command == 'price':
        # Test price discovery
        platform_metrics = {
            'daily_active_users': args.daily_users,
            'daily_revenue': args.daily_revenue,
            'initial_supply': 1_000_000_000,
            'development_cost': 2_000_000,
            'annual_operating_cost': 5_000_000
        }
        
        result = cli.test_price_discovery(platform_metrics)
        
        print("💰 Cold Start Price Discovery:")
        print(f"  Recommended Price: ${result['recommended_price']:.4f}")
        print(f"  Confidence Range: ${result['confidence_range'][0]:.4f} - ${result['confidence_range'][1]:.4f}")
        print("\n  Method Breakdown:")
        for method, price in result['method_breakdown'].items():
            print(f"    {method.replace('_', ' ').title()}: ${price:.4f}")
    
    elif args.command == 'simulate':
        # Run economic simulation
        scenario_params = {
            'daily_revenue': args.daily_revenue,
            'daily_users': args.daily_users,
            'creator_share': args.creator_share,
            'commission_burn_rate': args.burn_rate
        }
        
        result = cli.test_economic_scenario(scenario_params, args.days)
        
        print(f"📊 Economic Simulation ({args.days} days):")
        print(f"  Initial Price: ${result['initial_price']:.4f}")
        print(f"  Final Price: ${result['final_price']:.4f}")
        print(f"  Price Change: {result['price_change']:.1%}")
        print(f"  Supply Change: {result['supply_change']:.1%}")
        print(f"  Total Rewards: {result['total_rewards']:,.0f} VCOIN")
        print(f"  Total Burns: {result['total_burns']:,.0f} VCOIN")
        print(f"  Avg Creator Daily Earnings: {result['avg_daily_creator_earnings']:,.0f} VCOIN")
        print(f"  Economic Health Score: {result['economic_health']:.0f}/100")
    
    elif args.command == 'compare':
        # Compare two scenarios
        params_a = {
            'creator_share': 0.40,
            'commission_burn_rate': 0.50,
            'daily_revenue': args.daily_revenue,
            'daily_users': args.daily_users
        }
        
        params_b = {
            'creator_share': 0.45,
            'commission_burn_rate': 0.70,
            'daily_revenue': args.daily_revenue * 1.5,
            'daily_users': args.daily_users
        }
        
        result = cli.run_comparison_test(params_a, params_b)
        
        print("⚔️ A/B Scenario Comparison:")
        print("\nScenario A (Conservative):")
        print(f"  Final Price: ${result['scenario_a']['final_price']:.4f}")
        print(f"  Price Change: {result['scenario_a']['price_change']:.1%}")
        print(f"  Health Score: {result['scenario_a']['economic_health']:.0f}/100")
        
        print("\nScenario B (Creator-Friendly):")
        print(f"  Final Price: ${result['scenario_b']['final_price']:.4f}")
        print(f"  Price Change: {result['scenario_b']['price_change']:.1%}")
        print(f"  Health Score: {result['scenario_b']['economic_health']:.0f}/100")
        
        print("\nWinners:")
        for metric, winner in result['winners'].items():
            print(f"  {metric.replace('_', ' ').title()}: Scenario {winner}")
    
    # Save results if output specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")

if __name__ == "__main__":
    main()

# Example usage:
"""
# Test content reward calculation
python vcoin_cli_tester.py content --type podcast --views 5000 --shares 150 --likes 800 --comments 300 --creator-5a 420 --accuracy 95

# Test price discovery
python vcoin_cli_tester.py price --daily-revenue 50000 --daily-users 100000

# Run economic simulation
python vcoin_cli_tester.py simulate --days 180 --daily-revenue 75000 --creator-share 0.45 --burn-rate 0.70

# Compare scenarios
python vcoin_cli_tester.py compare --daily-revenue 50000 --daily-users 100000 --output comparison_results.json
"""
