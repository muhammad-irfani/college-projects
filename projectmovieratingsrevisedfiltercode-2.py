import pandas as pd
import matplotlib.pyplot as plt

# File paths (replace with your actual file paths)
file1 = r"C:\Users\kille\Documents\imdb_top_1000.csv"
file2 = r"C:\Users\kille\Documents\16k_Movies.csv"

# Columns to filter for each file
columns_to_keep_file1 = ['Series_Title', 'Released_Year', 'Runtime', 'Genre', 'IMDB_Rating', 'Director']
columns_to_keep_file2 = ['Title', 'Release Date', 'Rating', 'Directed by', 'Duration', 'Genres', 'No of Persons Voted']

# Read and filter the first file (IMDb data)
df1 = pd.read_csv(file1)
columns_to_keep_df1 = [col for col in columns_to_keep_file1 if col in df1.columns]
filtered_df1 = df1[columns_to_keep_df1].copy()

# Convert 'Released_Year' to numeric and filter for valid years
filtered_df1.loc[:, 'Released_Year'] = pd.to_numeric(filtered_df1['Released_Year'], errors='coerce')
filtered_df1 = filtered_df1.dropna(subset=['Released_Year'])

# Sort by IMDB_Rating
filtered_df1 = filtered_df1.sort_values(by='IMDB_Rating', ascending=False)

# Read and filter the second file (Metacritic data)
df2 = pd.read_csv(file2)
columns_to_keep_df2 = [col for col in columns_to_keep_file2 if col in df2.columns]
filtered_df2 = df2[columns_to_keep_df2].copy()

# Remove commas from 'No of Persons Voted' column
filtered_df2['No of Persons Voted'] = filtered_df2['No of Persons Voted'].str.replace(',', '')

# Ensure 'Rating' and 'No of Persons Voted' columns have numeric values
filtered_df2 = filtered_df2[pd.to_numeric(filtered_df2['Rating'], errors='coerce').notnull()]
filtered_df2 = filtered_df2[pd.to_numeric(filtered_df2['No of Persons Voted'], errors='coerce').notnull()]

# Convert 'No of Persons Voted' to numeric
filtered_df2['No of Persons Voted'] = pd.to_numeric(filtered_df2['No of Persons Voted'])

# REVISED Filter out entries with less than 300 'No of Persons Voted'
filtered_df2 = filtered_df2[filtered_df2['No of Persons Voted'] >= 300]

# REVISED Remove duplicate Titles
filtered_df2 = filtered_df2.drop_duplicates(subset='Title')

# Sort by Rating and No of Persons Voted
filtered_df2 = filtered_df2.sort_values(by=['Rating', 'No of Persons Voted'], ascending=[False, False])

# REVISED Extract 'Release_Year' from 'Release Date' in df2 for seasonal and decade analysis
df2['Release_Year'] = pd.to_datetime(df2['Release Date'], errors='coerce').dt.year

# REVISED Merge datasets on matching movie titles
merged_df = pd.merge(
    filtered_df1,
    filtered_df2,
    left_on='Series_Title',
    right_on='Title',
    how='inner',
    suffixes=('_IMDb', '_Metacritic')
)

# REVISED Calculate average rating for a combined perspective
merged_df['Average_Rating'] = (merged_df['IMDB_Rating'] + merged_df['Rating']) / 2

# REVISED Analyze seasonal trends by extracting release month
merged_df['Release_Month'] = pd.to_datetime(merged_df['Release Date'], errors='coerce').dt.month

# REVISED Analyze long-term trends by grouping data by decade
merged_df['Decade'] = (merged_df['Released_Year'] // 10) * 10

# REVISED Display the merged dataset
print("\nMerged DataFrame:")
print(merged_df.head())

# REVISED Export the merged data to a CSV file for further analysis
merged_df.to_csv(r"C:\Users\kille\Desktop\ISI 300\merged_movies_data.csv", index=False)

# REVISED Plotting: Top 10 Genres by Average Rating from the merged dataset
top_10_genre_avg_rating = merged_df.groupby('Genre')['Average_Rating'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 8))
top_10_genre_avg_rating.plot(kind='bar')
plt.xlabel('Genre')
plt.ylabel('Average Rating')
plt.title('Top 10 Genres by Average Rating (Merged Data)')
plt.show()

# REVISED Plotting: Top 10 Genres by IMDB Rating from the merged dataset
top_10_genre_imdb_rating = merged_df.groupby('Genre')['IMDB_Rating'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 8))
top_10_genre_imdb_rating.plot(kind='bar')
plt.xlabel('Genre')
plt.ylabel('IMDB Rating')
plt.title('Top 10 Genres by IMDB Rating (Merged Data)')
plt.show()


# -----------------------------------------------------------SECOND DATAFRAME-----------------------------------------------------------

# Create a second dataframe with only Rating, IMDB_Rating, Release Date, and Released_Year
second_df = merged_df[['Rating', 'IMDB_Rating', 'Release Date', 'Released_Year']]

# Print the second dataframe
print("Second dataframe:")
print(second_df)

# Save the second dataframe to a CSV file
second_output_file = r"C:\Users\kille\Desktop\ISI 300\second_movie_ratings.csv"
second_df.to_csv(second_output_file, index=False)

# Print confirmation
print(f"Second dataframe saved to {second_output_file}")