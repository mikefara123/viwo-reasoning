#!/usr/bin/env python3
"""
VCOIN Economic Simulation Engine
Core tokenomics algorithm for ViWo platform
"""

import math
import random
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

try:
    import numpy as np
except ImportError:
    print("Warning: numpy not installed. Some advanced features may not work.")
    np = None

@dataclass
class ContentMetrics:
    """Content performance metrics"""
    content_type: str  # 'podcast', 'long_video', 'short_video', 'text_post'
    view_count: int
    shares: int
    reports: int
    likes: int
    dislikes: int
    comments: int
    creator_5a_score: int  # 0-500
    accuracy_rating: int   # 0-100
    engagement_quality: int # 0-100
    duration_minutes: float = 0

@dataclass
class EconomicState:
    """Current economic state of the platform"""
    total_supply: int
    circulating_supply: int
    staked_supply: int
    current_price: float
    daily_revenue: float
    daily_active_users: int
    daily_content_count: int

class VCoinEconomicEngine:
    """Core economic simulation engine for VCOIN"""
    
    def __init__(self, initial_params: Dict[str, Any]):
        # Token supply parameters
        self.initial_supply = initial_params.get('initial_supply', 1_000_000_000)
        self.max_supply = initial_params.get('max_supply', 10_000_000_000)
        self.years_to_max = initial_params.get('years_to_max', 5)
        
        # Reward distribution parameters
        self.creator_share = initial_params.get('creator_share', 0.40)
        self.engagement_share = initial_params.get('engagement_share', 0.40)
        self.commission_share = initial_params.get('commission_share', 0.10)
        self.royalty_share = initial_params.get('royalty_share', 0.10)
        
        # Engagement breakdown (as % of total rewards)
        self.share_report_rate = initial_params.get('share_report_rate', 0.20)  # 20% of total
        self.like_dislike_rate = initial_params.get('like_dislike_rate', 0.10)  # 10% of total
        self.comment_rate = initial_params.get('comment_rate', 0.10)            # 10% of total
        
        # Quality parameters
        self.max_quality_multiplier = initial_params.get('max_quality_multiplier', 20.0)
        self.accuracy_bonus_rate = initial_params.get('accuracy_bonus_rate', 0.20)
        
        # Burn mechanism parameters
        self.commission_burn_rate = initial_params.get('commission_burn_rate', 0.50)
        self.nft_burn_rate = initial_params.get('nft_burn_rate', 0.30)
        self.promotion_burn_rate = initial_params.get('promotion_burn_rate', 1.00)
        
        # Content type multipliers
        self.content_multipliers = {
            'podcast': 3.0,      # Highest effort, longest engagement
            'long_video': 2.5,   # High production value
            'short_video': 1.5,  # Viral potential
            'text_post': 1.0     # Base rate
        }
        
        # Current economic state
        self.current_state = EconomicState(
            total_supply=self.initial_supply,
            circulating_supply=self.initial_supply,
            staked_supply=0,
            current_price=initial_params.get('initial_price', 0.10),
            daily_revenue=initial_params.get('daily_revenue', 50000),
            daily_active_users=initial_params.get('daily_users', 100000),
            daily_content_count=initial_params.get('daily_content', 5000)
        )
    
    def calculate_content_reward(self, content: ContentMetrics) -> Dict[str, float]:
        """
        Calculate total reward distribution for a piece of content
        """
        
        # Step 1: Calculate base reward
        base_reward = self._calculate_base_reward(content)
        
        # Step 2: Apply quality multipliers
        quality_multiplier = self._calculate_quality_multiplier(content)
        
        # Step 3: Calculate total reward
        total_reward = base_reward * quality_multiplier
        
        # Step 4: Distribute rewards according to allocation rules
        distribution = self._distribute_rewards(total_reward, content)
        
        return distribution
    
    def _calculate_base_reward(self, content: ContentMetrics) -> float:
        """Calculate base reward before quality multipliers"""
        
        # Daily reward pool (90% of revenue converted to VCOIN)
        daily_reward_pool = (self.current_state.daily_revenue * 0.90) / self.current_state.current_price
        
        # Base reward per content piece
        base_reward_per_content = daily_reward_pool / max(1, self.current_state.daily_content_count)
        
        # Apply content type multiplier
        content_multiplier = self.content_multipliers.get(content.content_type, 1.0)
        
        # Apply engagement factor (logarithmic to prevent gaming)
        total_engagement = content.shares + content.reports + content.likes + content.dislikes + content.comments
        engagement_factor = 1.0 + math.log10(max(1, total_engagement)) / 10
        
        # Apply view factor (logarithmic)
        view_factor = 1.0 + math.log10(max(1, content.view_count)) / 15
        
        base_reward = base_reward_per_content * content_multiplier * engagement_factor * view_factor
        
        return base_reward
    
    def _calculate_quality_multiplier(self, content: ContentMetrics) -> float:
        """Calculate quality-based reward multiplier"""
        
        # Creator 5A Score multiplier (0-500 scale)
        creator_5a_ranges = [
            (450, 500, 5.0),  # Elite creators
            (400, 449, 4.0),  # Expert creators  
            (350, 399, 3.0),  # Quality creators
            (300, 349, 2.0),  # Good creators
            (250, 299, 1.5),  # Average creators
            (200, 249, 1.0),  # Basic creators
            (0, 199, 0.5)     # Low quality (penalty)
        ]
        
        creator_multiplier = 1.0
        for min_score, max_score, multiplier in creator_5a_ranges:
            if min_score <= content.creator_5a_score <= max_score:
                creator_multiplier = multiplier
                break
        
        # Accuracy multiplier (0-100% scale)
        accuracy_multiplier = 0.5 + (content.accuracy_rating / 100) * 1.5  # Range: 0.5x to 2.0x
        
        # Engagement quality multiplier (0-100 scale)
        engagement_multiplier = 0.7 + (content.engagement_quality / 100) * 1.3  # Range: 0.7x to 2.0x
        
        # Combined multiplier (capped at max)
        total_multiplier = creator_multiplier * accuracy_multiplier * engagement_multiplier
        
        return min(self.max_quality_multiplier, max(0.1, total_multiplier))
    
    def _distribute_rewards(self, total_reward: float, content: ContentMetrics) -> Dict[str, float]:
        """Distribute total reward according to ViWo allocation rules"""
        
        # Apply accuracy bonus to creator share
        accuracy_bonus = 1.0 + (content.accuracy_rating / 100) * self.accuracy_bonus_rate
        
        # Base distribution
        creator_base_reward = total_reward * self.creator_share * accuracy_bonus
        
        # Engagement rewards distribution
        engagement_pool = total_reward * self.engagement_share
        
        # Calculate individual engagement rewards
        share_reward_pool = total_reward * 0.15  # 15% of total for shares
        report_reward_pool = total_reward * 0.05  # 5% of total for reports
        like_reward_pool = total_reward * 0.08    # 8% of total for likes
        dislike_reward_pool = total_reward * 0.02 # 2% of total for dislikes
        comment_reward_pool = total_reward * 0.10 # 10% of total for comments
        
        # Calculate per-action rewards
        share_per_action = share_reward_pool / max(1, content.shares)
        report_per_action = report_reward_pool / max(1, content.reports)
        like_per_action = like_reward_pool / max(1, content.likes)
        dislike_per_action = dislike_reward_pool / max(1, content.dislikes)
        comment_per_action = comment_reward_pool / max(1, content.comments)
        
        return {
            'total_reward': total_reward,
            'creator_reward': creator_base_reward,
            'share_reward_pool': share_reward_pool,
            'report_reward_pool': report_reward_pool,
            'like_reward_pool': like_reward_pool,
            'dislike_reward_pool': dislike_reward_pool,
            'comment_reward_pool': comment_reward_pool,
            'share_per_action': share_per_action,
            'report_per_action': report_per_action,
            'like_per_action': like_per_action,
            'dislike_per_action': dislike_per_action,
            'comment_per_action': comment_per_action,
            'platform_commission': total_reward * self.commission_share,
            'nft_royalty_pool': total_reward * self.royalty_share
        }
    
    def calculate_daily_burns(self, daily_activity: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """Calculate total daily token burns"""
        
        burns = {}
        
        # 1. Commission burns (% of platform commission)
        daily_commission = daily_activity.get('total_rewards', 0) * self.commission_share
        burns['commission_burn'] = daily_commission * self.commission_burn_rate
        
        # 2. NFT trading burns (% of NFT trading fees)
        nft_trading_volume = daily_activity.get('nft_volume', 0)
        nft_fees = nft_trading_volume * 0.05  # 5% trading fee
        burns['nft_burn'] = nft_fees * self.nft_burn_rate
        
        # 3. Content promotion burns (creators pay to boost visibility)
        promotion_spending = daily_activity.get('promotion_spending', 0)
        burns['promotion_burn'] = promotion_spending * self.promotion_burn_rate
        
        # 4. Governance burns (proposal submission fees)
        governance_proposals = daily_activity.get('governance_proposals', 0)
        burns['governance_burn'] = governance_proposals * 1000  # 1K VCOIN per proposal
        
        # 5. Quality bonus burns (fund exceptional content rewards)
        quality_bonus_pool = daily_activity.get('total_rewards', 0) * 0.05
        burns['quality_burn'] = quality_bonus_pool * 0.25
        
        total_daily_burn = sum(burns.values())
        
        return total_daily_burn, burns
    
    def simulate_day(self, day: int, user_activity: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate one day of platform economy"""
        
        # Update current state
        self.current_state.daily_active_users = user_activity.get('active_users', self.current_state.daily_active_users)
        self.current_state.daily_revenue = user_activity.get('revenue', self.current_state.daily_revenue)
        self.current_state.daily_content_count = user_activity.get('content_count', self.current_state.daily_content_count)
        
        # Calculate daily rewards for all content
        total_daily_rewards = 0
        content_rewards = []
        
        for content_data in user_activity.get('content_list', []):
            content = ContentMetrics(**content_data)
            reward_distribution = self.calculate_content_reward(content)
            content_rewards.append(reward_distribution)
            total_daily_rewards += reward_distribution['total_reward']
        
        # Calculate daily burns
        daily_activity_data = {
            'total_rewards': total_daily_rewards,
            'nft_volume': user_activity.get('nft_volume', total_daily_rewards * 0.05),
            'promotion_spending': user_activity.get('promotion_spending', total_daily_rewards * 0.02),
            'governance_proposals': user_activity.get('governance_proposals', max(1, self.current_state.daily_active_users // 10000))
        }
        
        total_burns, burn_breakdown = self.calculate_daily_burns(daily_activity_data)
        
        # Update token supply
        net_supply_change = total_daily_rewards - total_burns
        self.current_state.total_supply += net_supply_change
        self.current_state.circulating_supply += net_supply_change
        
        # Update token price (simplified price discovery)
        supply_pressure = net_supply_change / self.current_state.total_supply
        demand_pressure = user_activity.get('new_users', 0) / max(1, self.current_state.daily_active_users)
        
        price_change = (demand_pressure - supply_pressure) * 0.05  # 5% sensitivity
        self.current_state.current_price *= (1 + price_change)
        
        # Ensure price doesn't go negative
        self.current_state.current_price = max(0.001, self.current_state.current_price)
        
        return {
            'day': day,
            'total_supply': self.current_state.total_supply,
            'circulating_supply': self.current_state.circulating_supply,
            'current_price': self.current_state.current_price,
            'daily_rewards': total_daily_rewards,
            'daily_burns': total_burns,
            'net_supply_change': net_supply_change,
            'daily_revenue': self.current_state.daily_revenue,
            'active_users': self.current_state.daily_active_users,
            'content_count': self.current_state.daily_content_count,
            'content_rewards': content_rewards,
            'burn_breakdown': burn_breakdown,
            'inflation_rate': (net_supply_change / self.current_state.total_supply) * 365,  # Annualized
            'token_velocity': self._calculate_velocity(total_daily_rewards)
        }
    
    def _calculate_velocity(self, daily_transaction_volume: float) -> float:
        """Calculate token velocity"""
        active_supply = self.current_state.circulating_supply - self.current_state.staked_supply
        if active_supply <= 0:
            return 0
        
        daily_velocity = daily_transaction_volume / active_supply
        annual_velocity = daily_velocity * 365
        
        return annual_velocity
    
    def run_simulation(self, scenario_params: Dict[str, Any], days: int = 365) -> List[Dict[str, Any]]:
        """Run complete economic simulation for specified days"""
        
        results = []
        
        for day in range(days):
            # Generate user activity for this day
            user_activity = self._generate_user_activity(day, scenario_params)
            
            # Simulate day
            day_result = self.simulate_day(day, user_activity)
            results.append(day_result)
        
        return results
    
    def _generate_user_activity(self, day: int, scenario_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic user activity for simulation"""
        
        # User growth model (S-curve)
        max_users = scenario_params.get('max_users', 1_000_000)
        growth_rate = scenario_params.get('growth_rate', 0.008)
        current_users = max_users / (1 + math.exp(-growth_rate * (day - 365)))
        
        # Calculate new users
        prev_users = max_users / (1 + math.exp(-growth_rate * (day - 1 - 365))) if day > 0 else 0
        new_users = max(0, current_users - prev_users)
        
        # Content generation
        content_creation_rate = scenario_params.get('content_creation_rate', 0.05)  # 5% of users create
        daily_content_count = int(current_users * content_creation_rate)
        
        # Generate content distribution
        content_types = ['podcast', 'long_video', 'short_video', 'text_post']
        content_distribution = [0.05, 0.15, 0.60, 0.20]  # Distribution by type
        
        content_list = []
        for i in range(daily_content_count):
            content_type = random.choices(content_types, content_distribution)[0]
            content_metrics = self._generate_content_metrics(content_type, current_users)
            content_list.append(content_metrics)
        
        # Calculate platform revenue (grows with users)
        base_revenue = scenario_params.get('base_daily_revenue', 50000)
        revenue_growth_factor = (current_users / 100000) ** 0.8  # Sublinear growth
        daily_revenue = base_revenue * revenue_growth_factor
        
        return {
            'active_users': int(current_users),
            'new_users': int(new_users),
            'content_count': daily_content_count,
            'content_list': content_list,
            'revenue': daily_revenue,
            'nft_volume': daily_revenue * 0.05,      # 5% of revenue in NFT trading
            'promotion_spending': daily_revenue * 0.02,  # 2% spent on promotion
            'governance_proposals': max(1, int(current_users / 50000))  # 1 per 50K users
        }
    
    def _generate_content_metrics(self, content_type: str, total_users: int) -> Dict[str, Any]:
        """Generate realistic metrics for a piece of content"""
        
        # Base engagement rates by content type
        engagement_rates = {
            'podcast': 0.03,      # 3% of users engage with podcasts
            'long_video': 0.05,   # 5% engagement rate
            'short_video': 0.12,  # 12% engagement rate
            'text_post': 0.08     # 8% engagement rate
        }
        
        # Generate realistic view count
        potential_audience = int(total_users * 0.4)  # 40% could see content
        view_count = int(potential_audience * engagement_rates[content_type] * random.uniform(0.1, 5.0))
        
        # Generate engagement breakdown
        engagement_rate = random.uniform(0.05, 0.30)  # 5-30% of viewers engage
        total_engagement = int(view_count * engagement_rate)
        
        # Distribute engagement across actions
        shares = int(total_engagement * 0.15)      # 15% share
        reports = int(total_engagement * 0.03)     # 3% report
        likes = int(total_engagement * 0.65)       # 65% like
        dislikes = int(total_engagement * 0.07)    # 7% dislike  
        comments = int(total_engagement * 0.20)    # 20% comment
        
        # Generate quality scores
        creator_5a_score = random.randint(200, 500)
        accuracy_rating = random.randint(60, 100)
        engagement_quality = random.randint(40, 95)
        
        # Duration for time-based content
        duration_minutes = 0
        if content_type == 'podcast':
            duration_minutes = random.uniform(15, 120)
        elif content_type == 'long_video':
            duration_minutes = random.uniform(5, 60)
        elif content_type == 'short_video':
            duration_minutes = random.uniform(0.25, 5)
        
        return {
            'content_type': content_type,
            'view_count': view_count,
            'shares': shares,
            'reports': reports,
            'likes': likes,
            'dislikes': dislikes,
            'comments': comments,
            'creator_5a_score': creator_5a_score,
            'accuracy_rating': accuracy_rating,
            'engagement_quality': engagement_quality,
            'duration_minutes': duration_minutes
        }

class VCoinColdStartValuation:
    """Calculate initial VCOIN price using multiple valuation methods"""
    
    def __init__(self):
        self.valuation_weights = {
            'revenue_multiple': 0.25,
            'utility_value': 0.30,
            'comparable_analysis': 0.20,
            'cost_basis': 0.15,
            'network_value': 0.10
        }
    
    def calculate_initial_price(self, platform_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate fair initial VCOIN price using multiple methods"""
        
        valuations = {}
        
        # Method 1: Revenue Multiple Approach
        valuations['revenue_multiple'] = self._revenue_multiple_valuation(platform_metrics)
        
        # Method 2: Utility Value Approach
        valuations['utility_value'] = self._utility_value_valuation(platform_metrics)
        
        # Method 3: Comparable Analysis
        valuations['comparable_analysis'] = self._comparable_analysis_valuation(platform_metrics)
        
        # Method 4: Cost Basis Approach
        valuations['cost_basis'] = self._cost_basis_valuation(platform_metrics)
        
        # Method 5: Network Value (Metcalfe's Law)
        valuations['network_value'] = self._network_value_valuation(platform_metrics)
        
        # Calculate weighted average
        weighted_price = sum(
            valuations[method] * self.valuation_weights[method]
            for method in valuations.keys()
        )
        
        return {
            'recommended_price': weighted_price,
            'individual_valuations': valuations,
            'confidence_range': (weighted_price * 0.7, weighted_price * 1.3),
            'valuation_weights': self.valuation_weights
        }
    
    def _revenue_multiple_valuation(self, metrics: Dict[str, Any]) -> float:
        """Value based on revenue multiples of comparable platforms"""
        
        annual_revenue = metrics['daily_revenue'] * 365
        
        # Web3 social platforms trade at premium multiples
        web3_revenue_multiple = 15.0
        platform_valuation = annual_revenue * web3_revenue_multiple
        
        # Tokens represent utility layer (20-30% of platform value)
        token_layer_value = platform_valuation * 0.25
        
        # Price per token
        initial_supply = metrics.get('initial_supply', 1_000_000_000)
        price_per_token = token_layer_value / initial_supply
        
        return price_per_token
    
    def _utility_value_valuation(self, metrics: Dict[str, Any]) -> float:
        """Value based on utility requirements and usage"""
        
        # Required daily token flow for platform operations
        daily_token_volume = metrics['daily_revenue'] * 0.90  # 90% flows through tokens
        
        # Target velocity for healthy utility token (2-3x annually)
        target_velocity = 2.5
        
        # Required market cap to support daily volume
        required_market_cap = daily_token_volume * 365 / target_velocity
        
        # Price per token
        initial_supply = metrics.get('initial_supply', 1_000_000_000)
        utility_price = required_market_cap / initial_supply
        
        return max(0.01, min(1.0, utility_price))
    
    def _comparable_analysis_valuation(self, metrics: Dict[str, Any]) -> float:
        """Compare to existing Web3 social platforms"""
        
        # Comparable platforms (adjusted for current market conditions)
        comparables = {
            'friend_tech_peak': 3.50,
            'lens_protocol_implied': 0.25,
            'farcaster_implied': 0.15,
            'rally_peak': 0.45,
            'bitclout_peak': 1.20  # Before collapse
        }
        
        # Adjust for ViWo's superior monetization model
        # ViWo has day-1 monetization vs speculation-based models
        utility_premium = 0.3  # 30% premium for real utility
        
        # Take median and apply premium
        comparable_prices = list(comparables.values())
        median_price = sorted(comparable_prices)[len(comparable_prices)//2]
        
        adjusted_price = median_price * utility_premium
        
        return adjusted_price
    
    def _cost_basis_valuation(self, metrics: Dict[str, Any]) -> float:
        """Value based on development and operational costs"""
        
        # Platform development and operational costs
        development_cost = metrics.get('development_cost', 2_000_000)
        annual_operating_cost = metrics.get('annual_operating_cost', 5_000_000)
        
        # 3-year cost to establish sustainable platform
        total_platform_cost = development_cost + (annual_operating_cost * 3)
        
        # Tokens represent infrastructure access (30% of platform value)
        token_infrastructure_value = total_platform_cost * 0.30
        
        # Price per token
        initial_supply = metrics.get('initial_supply', 1_000_000_000)
        cost_basis_price = token_infrastructure_value / initial_supply
        
        return cost_basis_price
    
    def _network_value_valuation(self, metrics: Dict[str, Any]) -> float:
        """Metcalfe's Law: Value proportional to square of network size"""
        
        # Metcalfe's Law: V = k * n^2
        network_size = metrics['daily_active_users']
        
        # Conservative k value for new platform
        # (Twitter at peak: ~300M users, ~$40B value → k ≈ 0.00044)
        k_value = 0.0001
        
        network_value = k_value * (network_size ** 2)
        
        # Tokens represent portion of network value
        token_network_value = network_value * 0.20
        
        # Price per token
        initial_supply = metrics.get('initial_supply', 1_000_000_000)
        network_price = token_network_value / initial_supply
        
        return max(0.001, network_price)

# Example usage and testing
if __name__ == "__main__":
    # Initialize economic engine
    initial_params = {
        'initial_supply': 1_000_000_000,
        'max_supply': 10_000_000_000,
        'creator_share': 0.40,
        'engagement_share': 0.40,
        'commission_share': 0.10,
        'royalty_share': 0.10,
        'daily_revenue': 50000,
        'daily_users': 100000,
        'initial_price': 0.10
    }
    
    engine = VCoinEconomicEngine(initial_params)
    
    # Test individual content reward
    test_content = ContentMetrics(
        content_type='podcast',
        view_count=5000,
        shares=150,
        reports=25,
        likes=800,
        dislikes=50,
        comments=300,
        creator_5a_score=420,
        accuracy_rating=95,
        engagement_quality=85,
        duration_minutes=45
    )
    
    reward_result = engine.calculate_content_reward(test_content)
    
    print("🎯 Content Reward Calculation Example:")
    print(f"Total Reward: {reward_result['total_reward']:,.0f} VCOIN")
    print(f"Creator Reward: {reward_result['creator_reward']:,.0f} VCOIN")
    print(f"Platform Commission: {reward_result['platform_commission']:,.0f} VCOIN")
    print(f"Share Reward per Action: {reward_result['share_per_action']:,.2f} VCOIN")
    print(f"Comment Reward per Action: {reward_result['comment_per_action']:,.2f} VCOIN")
    
    # Test cold start valuation
    valuation_metrics = {
        'daily_revenue': 50000,
        'daily_active_users': 100000,
        'initial_supply': 1_000_000_000,
        'development_cost': 2_000_000,
        'annual_operating_cost': 5_000_000
    }
    
    valuator = VCoinColdStartValuation()
    valuation_result = valuator.calculate_initial_price(valuation_metrics)
    
    print(f"\n💰 Cold Start Valuation:")
    print(f"Recommended Price: ${valuation_result['recommended_price']:.4f}")
    print(f"Confidence Range: ${valuation_result['confidence_range'][0]:.4f} - ${valuation_result['confidence_range'][1]:.4f}")
    
    for method, price in valuation_result['individual_valuations'].items():
        weight = valuation_result['valuation_weights'][method]
        print(f"  {method.replace('_', ' ').title()}: ${price:.4f} (weight: {weight:.0%})")
