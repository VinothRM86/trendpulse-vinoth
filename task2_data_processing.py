import pandas as pd
import os

# Load JSON file
file_path = "data/trends_20260410.json"  

df = pd.read_json(file_path)

print("Loaded", len(df), "stories from", file_path)

#Cleaning

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# Remove rows with missing important values
df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# Remove extra spaces in title
df["title"] = df["title"].str.strip()

# Save CSV

output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print("\nSaved", len(df), "rows to", output_path)

# Summary (stories per category)

print("\nStories per category:")
print(df["category"].value_counts())