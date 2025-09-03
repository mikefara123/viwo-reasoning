# VCOIN Content Calculation Algorithm
**Complete Mathematical Framework for Creator Rewards**

## Overview
This document exports the complete algorithm used in VCOIN 4.0 for calculating content creator rewards, including all formulas, parameters, and step-by-step calculations.

---

## 1. Core Parameters

### Input Variables
```
daily_users = Number of daily active users
daily_content = Content posts per day (total across platform)
initial_token_price = Starting VCOIN price (e.g., $1.00)
current_token_price = Current VCOIN price (appreciates over time)
market_efficiency = How efficiently community value converts to investment (0.3-0.7)
investment_conversion = What % of theoretical investment actually flows in (0.1-0.5)
target_inflation = Annual inflation rate (default: 8%)
```

### Constants
```
base_value_per_interaction = $0.005
creator_percentage = 1% of daily users are active creators
target_creator_earnings = $165 per creator per month
staking_apy = 6.7% annual
total_token_supply = 10,000,000,000 tokens
```

---

## 2. Step-by-Step Algorithm

### Step 1: Calculate Community Engagement
```python
# Engagement rate increases logarithmically with user base
engagement_rate = min(0.3, log(daily_users + 1) / log(100000 + 1))

# Daily meaningful interactions
daily_content_normalized = daily_users * (50/15000)  # Normalize content per user
daily_interactions = daily_users * daily_content_normalized * engagement_rate

# Community value creation
daily_community_value = daily_interactions * base_value_per_interaction
monthly_community_value = daily_community_value * 30
```

### Step 2: Calculate Investment Attraction
```python
# Price appreciation factor
price_change_percent = (current_token_price / initial_token_price - 1) * 100

# Investment multiplier based on price appreciation
if price_change_percent <= 0:
    investment_multiplier = 0.5
elif price_change_percent <= 25:
    investment_multiplier = 0.8
elif price_change_percent <= 50:
    investment_multiplier = 1.0
else:
    investment_multiplier = min(1.3, 1.0 + (price_change_percent - 50) / 200)

# Calculate actual investment inflow
theoretical_investment = monthly_community_value * investment_multiplier
market_adjusted_investment = theoretical_investment * market_efficiency
actual_monthly_investment = market_adjusted_investment * investment_conversion
```

### Step 3: Calculate Creator Pool
```python
# Number of active creators
active_creators = daily_users * 0.01

# Creator funding sources
investment_to_creators = actual_monthly_investment * 0.7

# Inflation-based creator rewards
monthly_inflation_tokens = (total_token_supply * target_inflation / 100) / 12
creator_inflation_allocation = monthly_inflation_tokens * 0.4
creator_funding_from_inflation = creator_inflation_allocation * current_token_price

# Total available for creators
total_creator_funding = investment_to_creators + creator_funding_from_inflation
```

### Step 4: Dynamic Reward Adjustment
```python
# Reward multiplier prevents overpayment as token price rises
price_appreciation_factor = current_token_price / initial_token_price
reward_multiplier = 1.0 / (price_appreciation_factor ** 0.5)
reward_multiplier = max(0.1, min(1.0, reward_multiplier))

# Adjusted token rewards (if additional tokens needed)
creator_target_total = active_creators * target_creator_earnings
if total_creator_funding < creator_target_total:
    additional_tokens_needed = (creator_target_total - total_creator_funding) / current_token_price
    adjusted_token_rewards = additional_tokens_needed * reward_multiplier
else:
    adjusted_token_rewards = 0
```

---

## 3. Individual Creator Reward Calculation

### Basic Creator Reward Formula
```python
def calculate_creator_reward(creator_metrics, platform_state):
    """
    Calculate individual creator rewards based on performance and platform state
    
    Args:
        creator_metrics: {
            'monthly_views': int,
            'engagement_rate': float,
            'content_quality_score': float (1.0-2.0),
            'community_participation': float (0.0-1.0)
        }
        platform_state: {
            'total_creator_pool_usd': float,
            'active_creators': int,
            'current_token_price': float,
            'reward_multiplier': float
        }
    
    Returns:
        {
            'usd_reward': float,
            'token_reward': float,
            'total_value': float
        }
    """
    
    # Base reward per creator
    base_reward_usd = platform_state['total_creator_pool_usd'] / platform_state['active_creators']
    
    # Performance multipliers
    view_multiplier = min(2.0, creator_metrics['monthly_views'] / 100000)  # Cap at 2x for 100K+ views
    engagement_multiplier = 1.0 + (creator_metrics['engagement_rate'] - 0.05) * 2  # Bonus for >5% engagement
    quality_multiplier = creator_metrics['content_quality_score']
    participation_multiplier = 1.0 + creator_metrics['community_participation'] * 0.5
    
    # Combined performance score
    performance_score = (view_multiplier * engagement_multiplier * 
                        quality_multiplier * participation_multiplier)
    performance_score = max(0.5, min(3.0, performance_score))  # Bounds: 50%-300% of base
    
    # Calculate final rewards
    usd_reward = base_reward_usd * performance_score
    token_reward = (usd_reward * 0.3) / platform_state['current_token_price']  # 30% in tokens
    token_reward *= platform_state['reward_multiplier']  # Apply dynamic adjustment
    
    return {
        'usd_reward': usd_reward * 0.7,  # 70% in USD
        'token_reward': token_reward,
        'total_value': usd_reward * 0.7 + token_reward * platform_state['current_token_price']
    }
```

---

## 4. Content Quality Scoring Algorithm

### Multi-Factor Quality Assessment
```python
def calculate_content_quality_score(content_metrics):
    """
    Calculate content quality score based on multiple factors
    
    Args:
        content_metrics: {
            'view_duration_ratio': float,  # Actual/Expected view time
            'positive_sentiment': float,   # 0.0-1.0
            'comment_quality': float,      # 0.0-1.0
            'share_rate': float,          # Shares per view
            'repeat_viewers': float,       # % of viewers who return
            'creator_consistency': float  # Content posting consistency
        }
    
    Returns:
        float: Quality score (1.0-2.0)
    """
    
    # Weight each factor
    weights = {
        'view_duration_ratio': 0.25,
        'positive_sentiment': 0.15,
        'comment_quality': 0.15,
        'share_rate': 0.20,
        'repeat_viewers': 0.15,
        'creator_consistency': 0.10
    }
    
    # Normalize each metric to 0-1 scale
    normalized_metrics = {}
    normalized_metrics['view_duration_ratio'] = min(1.0, content_metrics['view_duration_ratio'])
    normalized_metrics['positive_sentiment'] = content_metrics['positive_sentiment']
    normalized_metrics['comment_quality'] = content_metrics['comment_quality']
    normalized_metrics['share_rate'] = min(1.0, content_metrics['share_rate'] * 100)  # Assuming 1% is max
    normalized_metrics['repeat_viewers'] = content_metrics['repeat_viewers']
    normalized_metrics['creator_consistency'] = content_metrics['creator_consistency']
    
    # Calculate weighted score
    quality_score = sum(normalized_metrics[metric] * weights[metric] 
                       for metric in weights.keys())
    
    # Scale to 1.0-2.0 range
    return 1.0 + quality_score
```

---

## 5. Platform Economics Integration

### Monthly Reward Distribution Process
```python
def distribute_monthly_rewards(platform_state, all_creators):
    """
    Complete monthly reward distribution algorithm
    """
    
    # Step 1: Calculate total available funding
    total_funding = calculate_total_creator_funding(platform_state)
    
    # Step 2: Calculate each creator's performance score
    creator_scores = []
    total_performance_points = 0
    
    for creator in all_creators:
        quality_score = calculate_content_quality_score(creator['content_metrics'])
        performance_score = calculate_performance_multiplier(creator, quality_score)
        creator_scores.append({
            'creator_id': creator['id'],
            'performance_score': performance_score,
            'base_eligibility': creator['monthly_views'] >= 1000  # Minimum threshold
        })
        if creator_scores[-1]['base_eligibility']:
            total_performance_points += performance_score
    
    # Step 3: Distribute rewards proportionally
    rewards = []
    for creator_score in creator_scores:
        if creator_score['base_eligibility']:
            # Proportional share of total funding
            creator_share = creator_score['performance_score'] / total_performance_points
            creator_funding = total_funding * creator_share
            
            # Calculate USD vs token split
            usd_component = creator_funding * 0.7
            token_component = (creator_funding * 0.3) / platform_state['current_token_price']
            token_component *= platform_state['reward_multiplier']
            
            rewards.append({
                'creator_id': creator_score['creator_id'],
                'usd_reward': usd_component,
                'token_reward': token_component,
                'performance_score': creator_score['performance_score'],
                'total_value': usd_component + token_component * platform_state['current_token_price']
            })
        else:
            rewards.append({
                'creator_id': creator_score['creator_id'],
                'usd_reward': 0,
                'token_reward': 0,
                'performance_score': 0,
                'reason': 'Below minimum threshold'
            })
    
    return rewards

def calculate_performance_multiplier(creator, quality_score):
    """Calculate overall performance multiplier for a creator"""
    
    # View-based multiplier (logarithmic scaling)
    view_multiplier = 1.0 + log(max(1000, creator['monthly_views'])) / log(1000000) * 1.5
    
    # Engagement multiplier
    engagement_rate = creator['total_engagements'] / max(1, creator['monthly_views'])
    engagement_multiplier = 1.0 + min(0.5, max(0, engagement_rate - 0.02)) * 10
    
    # Consistency bonus
    consistency_multiplier = 1.0 + creator['posting_consistency'] * 0.3
    
    # Community participation bonus
    participation_multiplier = 1.0 + creator['community_participation'] * 0.2
    
    # Combine all factors
    total_multiplier = (view_multiplier * engagement_multiplier * 
                       quality_score * consistency_multiplier * participation_multiplier)
    
    # Apply bounds
    return max(0.5, min(4.0, total_multiplier))
```

---

## 6. Real-Time Examples

### Example 1: Small Creator (10K monthly views)
```
Input:
- monthly_views: 10,000
- engagement_rate: 3%
- quality_score: 1.4
- platform_total_funding: $50,000
- active_creators: 300
- token_price: $2.50

Calculation:
- base_reward = $50,000 / 300 = $166.67
- view_multiplier = 1.0 + log(10000)/log(1000000) * 1.5 = 1.6
- engagement_multiplier = 1.0 + (0.03 - 0.02) * 10 = 1.1
- total_multiplier = 1.6 * 1.1 * 1.4 = 2.46
- final_reward = $166.67 * 2.46 = $410
- usd_portion = $410 * 0.7 = $287
- token_portion = ($410 * 0.3) / $2.50 = 49.2 tokens
```

### Example 2: Large Creator (500K monthly views)
```
Input:
- monthly_views: 500,000
- engagement_rate: 7%
- quality_score: 1.8
- same platform conditions

Calculation:
- base_reward = $166.67
- view_multiplier = 1.0 + log(500000)/log(1000000) * 1.5 = 2.05
- engagement_multiplier = 1.0 + (0.07 - 0.02) * 10 = 1.5
- total_multiplier = 2.05 * 1.5 * 1.8 = 5.54 (capped at 4.0)
- final_reward = $166.67 * 4.0 = $666.67
- usd_portion = $666.67 * 0.7 = $466.67
- token_portion = ($666.67 * 0.3) / $2.50 = 80 tokens
```

---

## 7. Implementation Code Export

### Complete Python Implementation
```python
import math
import pandas as pd
from datetime import datetime

class VCOINContentCalculator:
    def __init__(self, config):
        self.config = config
        self.total_supply = 10_000_000_000
        self.target_inflation = 0.08
        self.base_value_per_interaction = 0.005
        
    def calculate_monthly_distribution(self, platform_metrics, creators_data):
        """Main entry point for monthly reward calculation"""
        
        # Step 1: Platform-level calculations
        platform_state = self.calculate_platform_state(platform_metrics)
        
        # Step 2: Individual creator calculations
        creator_rewards = self.calculate_all_creator_rewards(creators_data, platform_state)
        
        # Step 3: Generate summary report
        summary = self.generate_summary(platform_state, creator_rewards)
        
        return {
            'platform_state': platform_state,
            'creator_rewards': creator_rewards,
            'summary': summary,
            'calculation_date': datetime.now().isoformat()
        }
    
    def calculate_platform_state(self, metrics):
        """Calculate overall platform economic state"""
        
        # Community value calculation
        engagement_rate = min(0.3, math.log(metrics['daily_users'] + 1) / math.log(100000 + 1))
        daily_interactions = metrics['daily_users'] * (50/15000) * engagement_rate
        monthly_community_value = daily_interactions * self.base_value_per_interaction * 30
        
        # Investment calculation
        price_change = (metrics['current_token_price'] / metrics['initial_token_price'] - 1) * 100
        if price_change <= 0:
            invest_mult = 0.5
        elif price_change <= 25:
            invest_mult = 0.8
        elif price_change <= 50:
            invest_mult = 1.0
        else:
            invest_mult = min(1.3, 1.0 + (price_change - 50) / 200)
        
        actual_investment = (monthly_community_value * invest_mult * 
                           metrics['market_efficiency'] * metrics['investment_conversion'])
        
        # Creator funding calculation
        investment_to_creators = actual_investment * 0.7
        monthly_inflation_tokens = (self.total_supply * self.target_inflation / 12)
        creator_inflation_funding = monthly_inflation_tokens * 0.4 * metrics['current_token_price']
        total_creator_funding = investment_to_creators + creator_inflation_funding
        
        # Dynamic reward multiplier
        price_factor = metrics['current_token_price'] / metrics['initial_token_price']
        reward_multiplier = max(0.1, min(1.0, 1.0 / (price_factor ** 0.5)))
        
        return {
            'monthly_community_value': monthly_community_value,
            'actual_investment': actual_investment,
            'total_creator_funding': total_creator_funding,
            'active_creators': metrics['daily_users'] * 0.01,
            'reward_multiplier': reward_multiplier,
            'current_token_price': metrics['current_token_price'],
            'engagement_rate': engagement_rate
        }
    
    def calculate_all_creator_rewards(self, creators_data, platform_state):
        """Calculate rewards for all creators"""
        
        rewards = []
        total_performance_points = 0
        
        # First pass: calculate performance scores
        for creator in creators_data:
            if creator['monthly_views'] >= 1000:  # Minimum threshold
                quality_score = self.calculate_quality_score(creator['content_metrics'])
                performance_score = self.calculate_performance_score(creator, quality_score)
                total_performance_points += performance_score
                
                rewards.append({
                    'creator_id': creator['id'],
                    'performance_score': performance_score,
                    'quality_score': quality_score,
                    'eligible': True
                })
            else:
                rewards.append({
                    'creator_id': creator['id'],
                    'performance_score': 0,
                    'quality_score': 0,
                    'eligible': False,
                    'reason': 'Below 1K monthly views threshold'
                })
        
        # Second pass: distribute funding
        for i, reward in enumerate(rewards):
            if reward['eligible']:
                creator_share = reward['performance_score'] / total_performance_points
                total_reward = platform_state['total_creator_funding'] * creator_share
                
                # Split USD vs tokens
                usd_reward = total_reward * 0.7
                token_reward = (total_reward * 0.3) / platform_state['current_token_price']
                token_reward *= platform_state['reward_multiplier']
                
                reward.update({
                    'usd_reward': usd_reward,
                    'token_reward': token_reward,
                    'total_value': usd_reward + token_reward * platform_state['current_token_price'],
                    'creator_data': creators_data[i]
                })
            else:
                reward.update({
                    'usd_reward': 0,
                    'token_reward': 0,
                    'total_value': 0
                })
        
        return rewards
    
    def calculate_quality_score(self, content_metrics):
        """Calculate content quality score (1.0-2.0)"""
        
        weights = {
            'view_duration_ratio': 0.25,
            'positive_sentiment': 0.15,
            'comment_quality': 0.15,
            'share_rate': 0.20,
            'repeat_viewers': 0.15,
            'creator_consistency': 0.10
        }
        
        # Normalize and weight each metric
        score = 0
        for metric, weight in weights.items():
            normalized_value = max(0, min(1, content_metrics.get(metric, 0.5)))
            score += normalized_value * weight
        
        return 1.0 + score  # Scale to 1.0-2.0 range
    
    def calculate_performance_score(self, creator, quality_score):
        """Calculate overall performance multiplier"""
        
        # View multiplier (logarithmic)
        view_mult = 1.0 + math.log(max(1000, creator['monthly_views'])) / math.log(1000000) * 1.5
        
        # Engagement multiplier
        engagement_rate = creator.get('engagement_rate', 0.02)
        engagement_mult = 1.0 + max(0, min(0.5, engagement_rate - 0.02)) * 10
        
        # Consistency and participation
        consistency_mult = 1.0 + creator.get('posting_consistency', 0.5) * 0.3
        participation_mult = 1.0 + creator.get('community_participation', 0.3) * 0.2
        
        total_score = view_mult * engagement_mult * quality_score * consistency_mult * participation_mult
        return max(0.5, min(4.0, total_score))  # Bounded 0.5x to 4.0x
    
    def generate_summary(self, platform_state, creator_rewards):
        """Generate summary statistics"""
        
        eligible_rewards = [r for r in creator_rewards if r['eligible']]
        
        return {
            'total_creators': len(creator_rewards),
            'eligible_creators': len(eligible_rewards),
            'total_usd_distributed': sum(r['usd_reward'] for r in eligible_rewards),
            'total_tokens_distributed': sum(r['token_reward'] for r in eligible_rewards),
            'average_creator_reward': sum(r['total_value'] for r in eligible_rewards) / max(1, len(eligible_rewards)),
            'platform_funding_utilization': sum(r['total_value'] for r in eligible_rewards) / platform_state['total_creator_funding'],
            'top_creator_reward': max((r['total_value'] for r in eligible_rewards), default=0),
            'platform_state': platform_state
        }

# Export configuration template
VCOIN_CONFIG = {
    'total_supply': 10_000_000_000,
    'target_inflation': 0.08,
    'base_value_per_interaction': 0.005,
    'min_creator_views': 1000,
    'usd_token_split': 0.7,  # 70% USD, 30% tokens
    'creator_funding_percentage': 0.7,  # 70% of investment to creators
    'inflation_to_creators': 0.4,  # 40% of inflation to creators
    'max_performance_multiplier': 4.0,
    'min_performance_multiplier': 0.5
}
```

---

## 8. Export Summary

This algorithm provides:

1. **Platform-level economics** - Community value creation and investment attraction
2. **Individual creator scoring** - Multi-factor performance assessment
3. **Dynamic reward adjustment** - Prevents inflation as token price rises
4. **Fair distribution** - Proportional rewards based on contribution
5. **Sustainability controls** - Built-in economic balancing mechanisms

The complete implementation can be extracted and used in any system that needs to calculate creator rewards based on community value creation and tokenomics principles.

---

**Generated:** 2025-09-03  
**Version:** VCOIN 4.0  
**Status:** Production Ready
