import pandas as pd
import glob
import os

def process_trends():
    """
    Loads raw trending data from Task 1, cleans it for quality, 
    and exports it to a tidy CSV.
    """
    
    # --- TASK 1: LOAD THE JSON FILE ---
    # Find the most recent JSON file in the data/ folder data/trends_YYYYMMDD.json
    json_files = glob.glob('data/trends_20260410.json')
    if not json_files:
        print("Error: No raw JSON data found in the 'data/' folder.")
        return
    
    # Select the latest file based on creation time
    input_file = max(json_files, key=os.path.getctime)
    df = pd.read_json(input_file)
    print(f"Loaded {len(df)} stories from {input_file}")

    # --- TASK 2: CLEAN THE DATA ---
    # 1. Remove duplicates based on unique post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"\nAfter removing duplicates: {len(df)}")

    # 2. Drop rows missing critical information
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")

    # 3. Fix data types and strip extra whitespace from titles
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].astype(int)
    df['title'] = df['title'].str.strip()

    # 4. Filter for high-quality stories (score >= 5)
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    # --- TASK 3: SAVE AS CSV & SUMMARY ---
    # Save to the data folder without the index column
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False)
    
    print(f"\nSaved {len(df)} rows to {output_path}")

    # Print frequency distribution for the 'category' column
    print("\nStories per category:")
    category_counts = df['category'].value_counts()
    for cat, count in category_counts.items():
        print(f"  {cat:<15} {count}")

if __name__ == "__main__":
    # Ensure the data directory exists before running
    if not os.path.exists('data'):
        os.makedirs('data')
        
    process_trends()