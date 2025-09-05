#!/usr/bin/env python3
"""
VCOIN Content Calculation Algorithm - Standalone Implementation
Complete algorithm for calculating creator rewards based on VCOIN 4.0 tokenomics
"""

import math
import json
from datetime import datetime
from typing import Dict, List, Any

class VCOINContentCalculator:
    """
    Standalone VCOIN content reward calculator
    Implements the complete algorithm from VCOIN 4.0
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize with configuration parameters"""
        self.config = config or self.get_default_config()
        
    def get_default_config(self) -> Dict[str, Any]:
        """Default configuration matching VCOIN 4.0 parameters"""
        return {
            'total_supply': 10_000_000_000,
            'target_inflation': 0.08,
            'base_value_per_interaction': 0.005,
            'min_creator_views': 1000,
            'usd_token_split': 0.7,
            'creator_funding_percentage': 0.7,
            'inflation_to_creators': 0.4,
            'max_performance_multiplier': 4.0,
            'min_performance_multiplier': 0.5,
            'creator_percentage': 0.01
        }
    
    def calculate_monthly_distribution(self, platform_metrics: Dict, creators_data: List[Dict]) -> Dict:
        """
        Main entry point for monthly reward calculation
        
        Args:
            platform_metrics: {
                'daily_users': int,
                'current_token_price': float,
                'initial_token_price': float,
                'market_efficiency': float (0.3-0.7),
                'investment_conversion': float (0.1-0.5)
            }
            creators_data: List of creator dictionaries with metrics
            
        Returns:
            Complete calculation results
        """
        
        # Step 1: Calculate platform-level state
        platform_state = self.calculate_platform_state(platform_metrics)
        
        # Step 2: Calculate individual creator rewards
        creator_rewards = self.calculate_all_creator_rewards(creators_data, platform_state)
        
        # Step 3: Generate summary
        summary = self.generate_summary(platform_state, creator_rewards)
        
        return {
            'platform_state': platform_state,
            'creator_rewards': creator_rewards,
            'summary': summary,
            'calculation_date': datetime.now().isoformat(),
            'config': self.config
        }
    
    def calculate_platform_state(self, metrics: Dict) -> Dict:
        """Calculate overall platform economic state"""
        
        daily_users = metrics['daily_users']
        current_price = metrics['current_token_price']
        initial_price = metrics['initial_token_price']
        market_efficiency = metrics['market_efficiency']
        investment_conversion = metrics['investment_conversion']
        
        # Step 1: Community value calculation
        engagement_rate = min(0.3, math.log(daily_users + 1) / math.log(100000 + 1))
        daily_content = daily_users * (50/15000)  # Normalized content per user
        daily_interactions = daily_users * daily_content * engagement_rate
        daily_community_value = daily_interactions * self.config['base_value_per_interaction']
        monthly_community_value = daily_community_value * 30
        
        # Step 2: Investment attraction calculation
        price_change_percent = (current_price / initial_price - 1) * 100
        
        if price_change_percent <= 0:
            investment_multiplier = 0.5
        elif price_change_percent <= 25:
            investment_multiplier = 0.8
        elif price_change_percent <= 50:
            investment_multiplier = 1.0
        else:
            investment_multiplier = min(1.3, 1.0 + (price_change_percent - 50) / 200)
        
        theoretical_investment = monthly_community_value * investment_multiplier
        market_adjusted_investment = theoretical_investment * market_efficiency
        actual_monthly_investment = market_adjusted_investment * investment_conversion
        
        # Step 3: Creator funding calculation
        investment_to_creators = actual_monthly_investment * self.config['creator_funding_percentage']
        
        # Inflation-based funding
        monthly_inflation_tokens = (self.config['total_supply'] * self.config['target_inflation']) / 12
        creator_inflation_allocation = monthly_inflation_tokens * self.config['inflation_to_creators']
        creator_funding_from_inflation = creator_inflation_allocation * current_price
        
        total_creator_funding = investment_to_creators + creator_funding_from_inflation
        
        # Step 4: Dynamic reward multiplier
        price_appreciation_factor = current_price / initial_price
        reward_multiplier = 1.0 / (price_appreciation_factor ** 0.5)
        reward_multiplier = max(0.1, min(1.0, reward_multiplier))
        
        # Step 5: Active creators count
        active_creators = daily_users * self.config['creator_percentage']
        
        return {
            'daily_users': daily_users,
            'engagement_rate': engagement_rate,
            'daily_interactions': daily_interactions,
            'monthly_community_value': monthly_community_value,
            'investment_multiplier': investment_multiplier,
            'actual_monthly_investment': actual_monthly_investment,
            'investment_to_creators': investment_to_creators,
            'creator_funding_from_inflation': creator_funding_from_inflation,
            'total_creator_funding': total_creator_funding,
            'active_creators': active_creators,
            'reward_multiplier': reward_multiplier,
            'current_token_price': current_price,
            'price_change_percent': price_change_percent
        }
    
    def calculate_all_creator_rewards(self, creators_data: List[Dict], platform_state: Dict) -> List[Dict]:
        """Calculate rewards for all creators"""
        
        rewards = []
        total_performance_points = 0
        
        # First pass: calculate performance scores and filter eligible creators
        for creator in creators_data:
            monthly_views = creator.get('monthly_views', 0)
            
            if monthly_views >= self.config['min_creator_views']:
                quality_score = self.calculate_quality_score(creator.get('content_metrics', {}))
                performance_score = self.calculate_performance_score(creator, quality_score)
                total_performance_points += performance_score
                
                rewards.append({
                    'creator_id': creator.get('id', 'unknown'),
                    'monthly_views': monthly_views,
                    'performance_score': performance_score,
                    'quality_score': quality_score,
                    'eligible': True
                })
            else:
                rewards.append({
                    'creator_id': creator.get('id', 'unknown'),
                    'monthly_views': monthly_views,
                    'performance_score': 0,
                    'quality_score': 0,
                    'eligible': False,
                    'reason': f'Below {self.config["min_creator_views"]} monthly views threshold'
                })
        
        # Second pass: distribute funding proportionally
        for reward in rewards:
            if reward['eligible'] and total_performance_points > 0:
                # Calculate proportional share
                creator_share = reward['performance_score'] / total_performance_points
                total_reward_value = platform_state['total_creator_funding'] * creator_share
                
                # Split between USD and tokens
                usd_reward = total_reward_value * self.config['usd_token_split']
                token_value = total_reward_value * (1 - self.config['usd_token_split'])
                token_reward = token_value / platform_state['current_token_price']
                
                # Apply dynamic reward multiplier to token portion
                token_reward *= platform_state['reward_multiplier']
                
                reward.update({
                    'total_reward_value': total_reward_value,
                    'usd_reward': usd_reward,
                    'token_reward': token_reward,
                    'final_total_value': usd_reward + (token_reward * platform_state['current_token_price'])
                })
            else:
                reward.update({
                    'total_reward_value': 0,
                    'usd_reward': 0,
                    'token_reward': 0,
                    'final_total_value': 0
                })
        
        return rewards
    
    def calculate_quality_score(self, content_metrics: Dict) -> float:
        """
        Calculate content quality score (1.0-2.0)
        
        Args:
            content_metrics: {
                'view_duration_ratio': float,
                'positive_sentiment': float,
                'comment_quality': float,
                'share_rate': float,
                'repeat_viewers': float,
                'creator_consistency': float
            }
        """
        
        weights = {
            'view_duration_ratio': 0.25,
            'positive_sentiment': 0.15,
            'comment_quality': 0.15,
            'share_rate': 0.20,
            'repeat_viewers': 0.15,
            'creator_consistency': 0.10
        }
        
        weighted_score = 0
        for metric, weight in weights.items():
            value = content_metrics.get(metric, 0.5)  # Default to 0.5 if missing
            normalized_value = max(0, min(1, value))  # Ensure 0-1 range
            weighted_score += normalized_value * weight
        
        return 1.0 + weighted_score  # Scale to 1.0-2.0 range
    
    def calculate_performance_score(self, creator: Dict, quality_score: float) -> float:
        """Calculate overall performance multiplier for a creator"""
        
        monthly_views = creator.get('monthly_views', 1000)
        engagement_rate = creator.get('engagement_rate', 0.02)
        posting_consistency = creator.get('posting_consistency', 0.5)
        community_participation = creator.get('community_participation', 0.3)
        
        # View multiplier (logarithmic scaling)
        view_multiplier = 1.0 + math.log(max(1000, monthly_views)) / math.log(1000000) * 1.5
        
        # Engagement multiplier (bonus for above 2% engagement)
        engagement_multiplier = 1.0 + max(0, min(0.5, engagement_rate - 0.02)) * 10
        
        # Consistency multiplier
        consistency_multiplier = 1.0 + posting_consistency * 0.3
        
        # Community participation multiplier
        participation_multiplier = 1.0 + community_participation * 0.2
        
        # Combine all factors
        total_multiplier = (view_multiplier * engagement_multiplier * 
                           quality_score * consistency_multiplier * participation_multiplier)
        
        # Apply bounds
        return max(self.config['min_performance_multiplier'], 
                  min(self.config['max_performance_multiplier'], total_multiplier))
    
    def generate_summary(self, platform_state: Dict, creator_rewards: List[Dict]) -> Dict:
        """Generate summary statistics"""
        
        eligible_rewards = [r for r in creator_rewards if r['eligible']]
        
        total_usd = sum(r['usd_reward'] for r in eligible_rewards)
        total_tokens = sum(r['token_reward'] for r in eligible_rewards)
        total_value = sum(r['final_total_value'] for r in eligible_rewards)
        
        return {
            'total_creators': len(creator_rewards),
            'eligible_creators': len(eligible_rewards),
            'ineligible_creators': len(creator_rewards) - len(eligible_rewards),
            'total_usd_distributed': total_usd,
            'total_tokens_distributed': total_tokens,
            'total_value_distributed': total_value,
            'average_creator_reward': total_value / max(1, len(eligible_rewards)),
            'median_creator_reward': self._calculate_median([r['final_total_value'] for r in eligible_rewards]),
            'top_creator_reward': max((r['final_total_value'] for r in eligible_rewards), default=0),
            'bottom_creator_reward': min((r['final_total_value'] for r in eligible_rewards if r['final_total_value'] > 0), default=0),
            'platform_funding_utilization': total_value / max(1, platform_state['total_creator_funding']),
            'average_performance_score': sum(r['performance_score'] for r in eligible_rewards) / max(1, len(eligible_rewards))
        }
    
    def _calculate_median(self, values: List[float]) -> float:
        """Calculate median value"""
        if not values:
            return 0
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 0:
            return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        else:
            return sorted_values[n//2]


def create_sample_data():
    """Create sample data for testing the algorithm"""
    
    platform_metrics = {
        'daily_users': 15000,
        'current_token_price': 2.50,
        'initial_token_price': 1.00,
        'market_efficiency': 0.5,
        'investment_conversion': 0.3
    }
    
    creators_data = [
        {
            'id': 'creator_001',
            'monthly_views': 50000,
            'engagement_rate': 0.05,
            'posting_consistency': 0.8,
            'community_participation': 0.6,
            'content_metrics': {
                'view_duration_ratio': 0.75,
                'positive_sentiment': 0.8,
                'comment_quality': 0.7,
                'share_rate': 0.02,
                'repeat_viewers': 0.4,
                'creator_consistency': 0.8
            }
        },
        {
            'id': 'creator_002',
            'monthly_views': 150000,
            'engagement_rate': 0.08,
            'posting_consistency': 0.9,
            'community_participation': 0.8,
            'content_metrics': {
                'view_duration_ratio': 0.85,
                'positive_sentiment': 0.9,
                'comment_quality': 0.85,
                'share_rate': 0.03,
                'repeat_viewers': 0.6,
                'creator_consistency': 0.9
            }
        },
        {
            'id': 'creator_003',
            'monthly_views': 5000,
            'engagement_rate': 0.03,
            'posting_consistency': 0.4,
            'community_participation': 0.2,
            'content_metrics': {
                'view_duration_ratio': 0.6,
                'positive_sentiment': 0.6,
                'comment_quality': 0.5,
                'share_rate': 0.01,
                'repeat_viewers': 0.2,
                'creator_consistency': 0.4
            }
        },
        {
            'id': 'creator_004',
            'monthly_views': 25000,
            'engagement_rate': 0.04,
            'posting_consistency': 0.7,
            'community_participation': 0.5,
            'content_metrics': {
                'view_duration_ratio': 0.7,
                'positive_sentiment': 0.75,
                'comment_quality': 0.6,
                'share_rate': 0.015,
                'repeat_viewers': 0.35,
                'creator_consistency': 0.7
            }
        }
    ]
    
    return platform_metrics, creators_data


def main():
    """Example usage of the VCOIN content calculator"""
    
    print("VCOIN Content Calculation Algorithm - Test Run")
    print("=" * 50)
    
    # Initialize calculator
    calculator = VCOINContentCalculator()
    
    # Create sample data
    platform_metrics, creators_data = create_sample_data()
    
    print(f"Platform: {platform_metrics['daily_users']:,} users, "
          f"${platform_metrics['current_token_price']:.2f} token price")
    print(f"Testing with {len(creators_data)} creators")
    print()
    
    # Run calculation
    results = calculator.calculate_monthly_distribution(platform_metrics, creators_data)
    
    # Display results
    print("PLATFORM STATE:")
    platform = results['platform_state']
    print(f"  Community Value: ${platform['monthly_community_value']:,.2f}/month")
    print(f"  Investment Inflow: ${platform['actual_monthly_investment']:,.2f}/month")
    print(f"  Creator Funding: ${platform['total_creator_funding']:,.2f}/month")
    print(f"  Reward Multiplier: {platform['reward_multiplier']:.3f}")
    print()
    
    print("CREATOR REWARDS:")
    for reward in results['creator_rewards']:
        if reward['eligible']:
            print(f"  {reward['creator_id']}: "
                  f"${reward['usd_reward']:.2f} USD + "
                  f"{reward['token_reward']:.1f} tokens = "
                  f"${reward['final_total_value']:.2f} total "
                  f"(score: {reward['performance_score']:.2f})")
        else:
            print(f"  {reward['creator_id']}: Not eligible - {reward['reason']}")
    print()
    
    print("SUMMARY:")
    summary = results['summary']
    print(f"  Total Distributed: ${summary['total_value_distributed']:,.2f}")
    print(f"  Average per Creator: ${summary['average_creator_reward']:,.2f}")
    print(f"  Eligible Creators: {summary['eligible_creators']}/{summary['total_creators']}")
    print(f"  Funding Utilization: {summary['platform_funding_utilization']:.1%}")
    print()
    
    # Export to JSON
    output_file = f"vcoin_calculation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results exported to: {output_file}")


if __name__ == "__main__":
    main()
