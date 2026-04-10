import pandas as pd
import numpy as np

# Load the CSV
file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print("Loaded data:", df.shape)

# Show first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score   :", int(avg_score))
print("Average comments:", int(avg_comments))

# -----------------------------------
# NumPy Analysis
# -----------------------------------

scores = df["score"].values   # convert to NumPy array

print("\n--- NumPy Stats ---")

print("Mean score   :", int(np.mean(scores)))
print("Median score :", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))

print("Max score    :", int(np.max(scores)))
print("Min score    :", int(np.min(scores)))

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()

print("\nMost stories in:", top_category, f"({category_counts[top_category]} stories)")

# Story with most comments
max_comments_row = df.loc[df["num_comments"].idxmax()]

print("\nMost commented story:")
print(f'"{max_comments_row["title"]}" — {max_comments_row["num_comments"]} comments')

# -----------------------------------
# Add New Columns
# -----------------------------------

# Engagement column
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular column
df["is_popular"] = df["score"] > avg_score

# -----------------------------------
# Save File
# -----------------------------------

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print("\nSaved to", output_path)