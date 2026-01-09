import pandas as pd
import json

def create_csv(data_list, filename="results.csv"):
    if not data_list:
        print("⚠ No data to save.")
        return

    # Create one master DataFrame
    df = pd.DataFrame(data_list)
    
    # Save to CSV (index=False removes the 0,1,2 row numbers)
    #df.to_csv(filename, index=False)
    
    #print(f"\n✅ Success! Saved {len(df)} rows to '{filename}'")
    print("Preview:")
    print(df.head())



