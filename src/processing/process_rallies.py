#!/usr/bin/env python3
"""
Process badminton match data to extract rally information.

This script processes CSV files from match directories in data/raw/ and creates
a consolidated rallies file with the following fields:
- match: Name of the match
- server: Who served (A or B)
- winner: Who won the rally (A or B) 
- duration: Number of shots in the rally
- serve_type: Type of serve (short_service or long_service)
- win_reason: Reason for winning (from the last shot's win_reason field)
"""

import os
import pandas as pd
import glob
from pathlib import Path
import re

def map_serve_type(serve_type):
    """Map Chinese serve types to English."""
    if serve_type == "發短球":
        return "short_service"
    elif serve_type == "發長球":
        return "long_service"
    else:
        return serve_type  # Keep original if not recognized

def map_win_reason(win_reason):
    """Map Chinese win reasons to English."""
    mapping = {
        "對手出界": "opponent hits out of bounds",
        "落地致勝": "shuttle hits opponents court", 
        "對手掛網": "opponent hits net",
        "對手未過網": "opponent hits into net",
        "對手落點判斷失誤": "opponent misjudged in court"
    }
    return mapping.get(win_reason, win_reason)  # Keep original if not in mapping

def process_match_file(file_path):
    """Process a single match CSV file and extract rally data."""
    try:
        df = pd.read_csv(file_path)
        
        # Group by rally number to process each rally
        rallies = []
        
        for rally_num in df['rally'].unique():
            rally_data = df[df['rally'] == rally_num].copy()
            
            # Find the actual serve (server=1) to determine server and serve type
            serve_shot = rally_data[rally_data['server'] == 1]
            if len(serve_shot) == 0:
                continue  # Skip rallies without a proper serve
            
            serve_shot = serve_shot.iloc[0]
            server = serve_shot['player']  # The player who serves
            serve_type_raw = serve_shot['type']
            serve_type = map_serve_type(serve_type_raw)
            
            # Get the last shot to determine winner and win reason
            last_shot = rally_data.iloc[-1]
            winner = last_shot['getpoint_player']
            win_reason_raw = last_shot['win_reason']
            win_reason = map_win_reason(win_reason_raw)
            
            # Calculate duration (number of shots)
            duration = len(rally_data)
            
            # Extract match info from file path
            match_name = os.path.basename(os.path.dirname(file_path))
            
            rally_info = {
                'match': match_name,
                'rally': rally_num,
                'server': server,
                'winner': winner,
                'duration': duration,
                'serve_type': serve_type,
                'win_reason': win_reason
            }
            
            rallies.append(rally_info)
        
        return rallies
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def process_all_matches():
    """Process all match directories and create consolidated rallies file."""
    
    # Create output directory if it doesn't exist
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all CSV files in match directories
    raw_dir = Path("data/raw")
    csv_files = []
    
    for match_dir in raw_dir.iterdir():
        if match_dir.is_dir() and not match_dir.name.endswith('.csv'):
            # Look for CSV files in this match directory
            for csv_file in match_dir.glob("*.csv"):
                csv_files.append(csv_file)
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    all_rallies = []
    
    for csv_file in csv_files:
        print(f"Processing: {csv_file}")
        rallies = process_match_file(csv_file)
        all_rallies.extend(rallies)
    
    # Create DataFrame and save
    if all_rallies:
        df_rallies = pd.DataFrame(all_rallies)
        
        # Save to CSV
        output_file = output_dir / "rallies.csv"
        df_rallies.to_csv(output_file, index=False)
        
        print(f"\nProcessing complete!")
        print(f"Total rallies processed: {len(all_rallies)}")
        print(f"Output saved to: {output_file}")
        
        # Display sample of the data
        print(f"\nSample data:")
        print(df_rallies.head(10))
        
        # Display summary statistics
        print(f"\nSummary statistics:")
        print(f"Rallies by serve type:")
        print(df_rallies['serve_type'].value_counts())
        print(f"\nRallies by winner:")
        print(df_rallies['winner'].value_counts())
        print(f"\nAverage rally duration: {df_rallies['duration'].mean():.2f} shots")
        
    else:
        print("No rallies found to process")

if __name__ == "__main__":
    process_all_matches()
