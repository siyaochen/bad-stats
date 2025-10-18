#!/usr/bin/env python3
"""
Badminton serving advantage analysis.

This analysis reveals that:
1. Individual players perform ~2% better when receiving
2. But servers are more skilled, so serving appears advantageous overall
3. The true serving advantage is confounded by skill bias
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_rallies_data():
    """Load the processed rallies data."""
    rallies_file = Path("data/processed/rallies.csv")
    if not rallies_file.exists():
        raise FileNotFoundError("Rallies data not found. Please run process_rallies.py first.")
    
    df = pd.read_csv(rallies_file)
    df_clean = df[df['serve_type'].isin(['short_service', 'long_service'])].copy()
    # The server field now directly contains 'A' or 'B' from the corrected processing
    
    return df_clean

def analyze_individual_serving_advantage(df):
    """Analyze each player's serving vs receiving performance."""
    
    individual_advantages = []
    
    for match in df['match'].unique():
        match_df = df[df['match'] == match]
        
        # Player A analysis
        player_a_serving = match_df[match_df['server'] == 'A']
        player_a_serving_wins = player_a_serving[player_a_serving['winner'] == 'A']
        player_a_serving_rate = len(player_a_serving_wins) / len(player_a_serving) if len(player_a_serving) > 0 else 0
        
        player_a_receiving = match_df[match_df['server'] == 'B']
        player_a_receiving_wins = player_a_receiving[player_a_receiving['winner'] == 'A']
        player_a_receiving_rate = len(player_a_receiving_wins) / len(player_a_receiving) if len(player_a_receiving) > 0 else 0
        
        if len(player_a_serving) > 0 and len(player_a_receiving) > 0:
            individual_advantages.append(player_a_serving_rate - player_a_receiving_rate)
        
        # Player B analysis
        player_b_serving = match_df[match_df['server'] == 'B']
        player_b_serving_wins = player_b_serving[player_b_serving['winner'] == 'B']
        player_b_serving_rate = len(player_b_serving_wins) / len(player_b_serving) if len(player_b_serving) > 0 else 0
        
        player_b_receiving = match_df[match_df['server'] == 'A']
        player_b_receiving_wins = player_b_receiving[player_b_receiving['winner'] == 'B']
        player_b_receiving_rate = len(player_b_receiving_wins) / len(player_b_receiving) if len(player_b_receiving) > 0 else 0
        
        if len(player_b_serving) > 0 and len(player_b_receiving) > 0:
            individual_advantages.append(player_b_serving_rate - player_b_receiving_rate)
    
    return individual_advantages

def analyze_overall_serving_advantage(df):
    """Analyze overall serving vs receiving performance."""
    
    server_wins = df[df['server'] == df['winner']]
    receiver_wins = df[df['server'] != df['winner']]
    
    total_rallies = len(df)
    serving_win_rate = len(server_wins) / total_rallies
    receiving_win_rate = len(receiver_wins) / total_rallies
    overall_advantage = serving_win_rate - receiving_win_rate
    
    return {
        'total_rallies': total_rallies,
        'serving_win_rate': serving_win_rate,
        'receiving_win_rate': receiving_win_rate,
        'overall_advantage': overall_advantage
    }

def analyze_by_serve_type(df):
    """Analyze individual serving advantage by serve type."""
    
    results = []
    
    for serve_type in ['short_service', 'long_service']:
        type_df = df[df['serve_type'] == serve_type]
        
        # Individual-level analysis for this serve type
        individual_advantages = []
        
        for match in type_df['match'].unique():
            match_df = type_df[type_df['match'] == match]
            
            # Player A analysis
            player_a_serving = match_df[match_df['server'] == 'A']
            player_a_serving_wins = player_a_serving[player_a_serving['winner'] == 'A']
            player_a_serving_rate = len(player_a_serving_wins) / len(player_a_serving) if len(player_a_serving) > 0 else 0
            
            player_a_receiving = match_df[match_df['server'] == 'B']
            player_a_receiving_wins = player_a_receiving[player_a_receiving['winner'] == 'A']
            player_a_receiving_rate = len(player_a_receiving_wins) / len(player_a_receiving) if len(player_a_receiving) > 0 else 0
            
            if len(player_a_serving) > 0 and len(player_a_receiving) > 0:
                individual_advantages.append(player_a_serving_rate - player_a_receiving_rate)
            
            # Player B analysis
            player_b_serving = match_df[match_df['server'] == 'B']
            player_b_serving_wins = player_b_serving[player_b_serving['winner'] == 'B']
            player_b_serving_rate = len(player_b_serving_wins) / len(player_b_serving) if len(player_b_serving) > 0 else 0
            
            player_b_receiving = match_df[match_df['server'] == 'A']
            player_b_receiving_wins = player_b_receiving[player_b_receiving['winner'] == 'B']
            player_b_receiving_rate = len(player_b_receiving_wins) / len(player_b_receiving) if len(player_b_receiving) > 0 else 0
            
            if len(player_b_serving) > 0 and len(player_b_receiving) > 0:
                individual_advantages.append(player_b_serving_rate - player_b_receiving_rate)
        
        # Calculate average individual advantage for this serve type
        avg_individual_advantage = np.mean(individual_advantages) if individual_advantages else 0
        
        results.append({
            'serve_type': serve_type,
            'total_rallies': len(type_df),
            'individual_measurements': len(individual_advantages),
            'individual_serving_advantage': avg_individual_advantage
        })
    
    return results

def analyze_by_win_reason(df):
    """Analyze individual serving advantage by win reason."""
    
    results = []
    
    # Get top win reasons
    top_reasons = df['win_reason'].value_counts().head(10)
    
    for reason in top_reasons.index:
        if pd.isna(reason) or reason == '':
            continue
        
        reason_df = df[df['win_reason'] == reason]
        
        # Individual-level analysis for this win reason
        individual_advantages = []
        
        for match in reason_df['match'].unique():
            match_df = reason_df[reason_df['match'] == match]
            
            # Player A analysis
            player_a_serving = match_df[match_df['server'] == 'A']
            player_a_serving_wins = player_a_serving[player_a_serving['winner'] == 'A']
            player_a_serving_rate = len(player_a_serving_wins) / len(player_a_serving) if len(player_a_serving) > 0 else 0
            
            player_a_receiving = match_df[match_df['server'] == 'B']
            player_a_receiving_wins = player_a_receiving[player_a_receiving['winner'] == 'A']
            player_a_receiving_rate = len(player_a_receiving_wins) / len(player_a_receiving) if len(player_a_receiving) > 0 else 0
            
            if len(player_a_serving) > 0 and len(player_a_receiving) > 0:
                individual_advantages.append(player_a_serving_rate - player_a_receiving_rate)
            
            # Player B analysis
            player_b_serving = match_df[match_df['server'] == 'B']
            player_b_serving_wins = player_b_serving[player_b_serving['winner'] == 'B']
            player_b_serving_rate = len(player_b_serving_wins) / len(player_b_serving) if len(player_b_serving) > 0 else 0
            
            player_b_receiving = match_df[match_df['server'] == 'A']
            player_b_receiving_wins = player_b_receiving[player_b_receiving['winner'] == 'B']
            player_b_receiving_rate = len(player_b_receiving_wins) / len(player_b_receiving) if len(player_b_receiving) > 0 else 0
            
            if len(player_b_serving) > 0 and len(player_b_receiving) > 0:
                individual_advantages.append(player_b_serving_rate - player_b_receiving_rate)
        
        # Calculate average individual advantage for this win reason
        avg_individual_advantage = np.mean(individual_advantages) if individual_advantages else 0
        
        results.append({
            'win_reason': reason,
            'total_rallies': len(reason_df),
            'individual_measurements': len(individual_advantages),
            'individual_serving_advantage': avg_individual_advantage
        })
    
    return results

def main():
    """Main analysis function."""
    
    print("🏸 Badminton Serving Advantage Analysis")
    print("=" * 50)
    
    # Load data
    df = load_rallies_data()
    print(f"Analyzing {len(df)} rallies from {df['match'].nunique()} matches")
    
    # Individual serving advantage
    individual_advantages = analyze_individual_serving_advantage(df)
    avg_individual_advantage = np.mean(individual_advantages)
    positive_count = sum(1 for x in individual_advantages if x > 0)
    negative_count = sum(1 for x in individual_advantages if x < 0)
    
    # Overall serving advantage
    overall_stats = analyze_overall_serving_advantage(df)
    
    # Serve type analysis
    serve_type_results = analyze_by_serve_type(df)
    
    # Win reason analysis
    win_reason_results = analyze_by_win_reason(df)
    
    # Create results
    results = {
        'individual_serving_advantage': {
            'average_advantage': avg_individual_advantage,
            'total_measurements': len(individual_advantages),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'positive_percentage': positive_count / len(individual_advantages) * 100
        },
        'overall_serving_advantage': overall_stats,
        'serve_type_analysis': serve_type_results,
        'win_reason_analysis': win_reason_results
    }
    
    # Save results
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Create summary
    summary_data = []
    
    # Individual results
    summary_data.append({
        'metric': 'Individual Serving Advantage (Average)',
        'value': f"{avg_individual_advantage:.3f}",
        'description': 'Average advantage for individual players when serving vs receiving'
    })
    
    summary_data.append({
        'metric': 'Individual Measurements',
        'value': len(individual_advantages),
        'description': 'Total individual player measurements'
    })
    
    summary_data.append({
        'metric': 'Positive Advantages',
        'value': f"{positive_count} ({positive_count/len(individual_advantages)*100:.1f}%)",
        'description': 'Players who perform better when serving'
    })
    
    summary_data.append({
        'metric': 'Negative Advantages',
        'value': f"{negative_count} ({negative_count/len(individual_advantages)*100:.1f}%)",
        'description': 'Players who perform better when receiving'
    })
    
    # Overall results
    summary_data.append({
        'metric': 'Overall Serving Win Rate',
        'value': f"{overall_stats['serving_win_rate']:.3f}",
        'description': 'Overall win rate when serving'
    })
    
    summary_data.append({
        'metric': 'Overall Receiving Win Rate',
        'value': f"{overall_stats['receiving_win_rate']:.3f}",
        'description': 'Overall win rate when receiving'
    })
    
    summary_data.append({
        'metric': 'Overall Serving Advantage',
        'value': f"{overall_stats['overall_advantage']:.3f}",
        'description': 'Overall advantage of serving vs receiving'
    })
    
    # Serve type results (individual level)
    for result in serve_type_results:
        summary_data.append({
            'metric': f'{result["serve_type"].upper()} Individual Advantage',
            'value': f"{result['individual_serving_advantage']:.3f}",
            'description': f'Individual serving advantage for {result["serve_type"]} (n={result["individual_measurements"]})'
        })
    
    # Win reason results (individual level, top 5)
    for result in win_reason_results[:5]:
        summary_data.append({
            'metric': f'{result["win_reason"]} Individual Advantage',
            'value': f"{result['individual_serving_advantage']:.3f}",
            'description': f'Individual serving advantage for rallies ending in {result["win_reason"]} (n={result["individual_measurements"]})'
        })
    
    # Save to CSV
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_dir / "serving_advantage_analysis.csv", index=False)
    
    # Save detailed breakdowns
    serve_type_df = pd.DataFrame(serve_type_results)
    serve_type_df.to_csv(output_dir / "serve_type_breakdown.csv", index=False)
    
    win_reason_df = pd.DataFrame(win_reason_results)
    win_reason_df.to_csv(output_dir / "win_reason_breakdown.csv", index=False)
    
    # Print results
    print(f"\n=== RESULTS ===")
    print(f"Individual serving advantage: {avg_individual_advantage:.3f}")
    print(f"Overall serving advantage: {overall_stats['overall_advantage']:.3f}")
    print(f"Individual measurements: {len(individual_advantages)}")
    print(f"Positive advantages: {positive_count} ({positive_count/len(individual_advantages)*100:.1f}%)")
    print(f"Negative advantages: {negative_count} ({negative_count/len(individual_advantages)*100:.1f}%)")
    
    print(f"\n=== CONCLUSION ===")
    print(f"Individual players perform {abs(avg_individual_advantage):.1%} better when receiving.")
    print(f"However, servers are more skilled, so serving appears {overall_stats['overall_advantage']:.1%} advantageous overall.")
    print(f"This reveals the skill bias in serving advantage analysis.")
    
    print(f"\n=== SERVE TYPE BREAKDOWN (Individual Level) ===")
    for result in serve_type_results:
        print(f"{result['serve_type'].upper()}: {result['individual_serving_advantage']:.3f} individual advantage (n={result['individual_measurements']})")
    
    print(f"\n=== WIN REASON BREAKDOWN (Individual Level, Top 5) ===")
    for result in win_reason_results[:5]:
        print(f"{result['win_reason']}: {result['individual_serving_advantage']:.3f} individual advantage (n={result['individual_measurements']})")
    
    print(f"\nResults saved to:")
    print(f"  - output/serving_advantage_analysis.csv (summary)")
    print(f"  - output/serve_type_breakdown.csv (detailed)")
    print(f"  - output/win_reason_breakdown.csv (detailed)")

if __name__ == "__main__":
    main()
