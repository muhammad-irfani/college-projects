import numpy as np
import pandas as pd

# Read CSV file into pandas dataframe
IEA_df = pd.read_csv('/Users/muhammadirfani/Desktop/F2024/ISI 300/IEA Global EV Data 2024.csv')

# Print shape of dataframe to check if it has been read in correctly
print(IEA_df.shape)

# Filter out rows with unit of "percent"
IEA_df = IEA_df[IEA_df.unit != 'percent']

# Print shape of dataframe to check if rows have been deleted
print(IEA_df.shape)

# Filter out rows with regions other than specific countries
IEA_df = IEA_df[IEA_df.region.isin(['USA', 'China', 'Germany', 'United Kingdom', 'France', 'Norway', 'Iceland', 'Netherlands'])]

# Print shape of dataframe to check if rows have been deleted
print(IEA_df.shape)

# Prompt user to input desired years for filtering
desired_years = []
print("Enter the years you want to filter data for (type 'done' when finished):")
while True:
    year = input("Enter a year: ").strip()
    if year.lower() == 'done':
        break
    if year.isdigit():
        desired_years.append(int(year))
    else:
        print("Invalid input. Please enter a valid year or 'done'.")

# Filter IEA_df based on user-specified years
if desired_years:
    IEA_df = IEA_df[IEA_df.year.isin(desired_years)]
    print(f"Filtered data for years: {desired_years}")
else:
    print("No years specified. Data will not be filtered by year.")

# Eliminate column "mode" in IEA_df
IEA_df = IEA_df.drop(columns=['mode'])

# Combine rows with the same region, category, parameter, powertrain, year, and unit, summing their value column
IEA_df = IEA_df.groupby(['region', 'category', 'parameter', 'powertrain', 'year', 'unit']).sum().reset_index()
print(IEA_df.head())

# Remove rows with parameter "EV charging points" in IEA_df
IEA_df = IEA_df[IEA_df.parameter != 'EV charging points']

# If the region, category, parameter, powertrain, and unit are the same, calculate the difference in value between years
IEA_df = IEA_df.pivot_table(index=['region', 'category', 'parameter', 'powertrain', 'unit'], columns='year', values='value', fill_value=0).reset_index()
if len(desired_years) > 1:  # Calculate the difference only if more than one year exists
    max_year = max(desired_years)
    min_year = min(desired_years)
    IEA_df['value_diff'] = IEA_df[max_year] - IEA_df[min_year]
print(IEA_df.head())

# Remove rows without parameter "EV Sales" in IEA_df
IEA_df = IEA_df[IEA_df.parameter == 'EV sales']

# Remove rows with category other than "Historical" in IEA_df
IEA_df = IEA_df[IEA_df.category == 'Historical']

# Save filtered IEA_df as an Excel file
IEA_df.to_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/IEA_EV_Sales_Years_Filtered.xlsx', index=False)

# Input the saved file back into a pandas dataframe
IEA_cleaned_df = pd.read_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/IEA_EV_Sales_Years_Filtered.xlsx')

# Remove rows with powertrain other than BEV in IEA_cleaned_df
IEA_cleaned_df = IEA_cleaned_df[IEA_cleaned_df.powertrain == 'BEV']
print(IEA_cleaned_df.head())

# Read additional Excel sheets
df_BEV = pd.read_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/Global_Data_EV.xlsx', sheet_name='BEV')
df_BEV = df_BEV.rename(columns={'Country/area': 'region'})

# Read Sales by Brand Excel file
Sales_Brand_df = pd.read_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/EV_Sales_By_Brand.xlsx')

# Print first 5 rows of Sales_Brand_df to check if it has been read in correctly
print(Sales_Brand_df.head())

# Read additional sheets for PHEV and New Cars Sold
df_PHEV = pd.read_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/Global_Data_EV.xlsx', sheet_name='PHEV')
print(df_PHEV.head(3))

df_NCS = pd.read_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/Global_Data_EV.xlsx', sheet_name='New Cars Sold')
print(df_NCS.head(3))

# Merge IEA_cleaned_df and df_BEV on region
merged_df = pd.merge(IEA_cleaned_df, df_BEV, on='region', how='inner')

# Save the merged dataframe as an Excel file
merged_df.to_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/Merged_IEA_BEV_Sales.xlsx', index=False)

# Load the population data from the uploaded CSV
population_df = pd.read_csv('/mnt/data/world_population.csv')

# Print the first few rows of the population data to understand its structure
print(population_df.head())

# Merge the population data with the IEA_cleaned_df on the 'region' column
IEA_population_merged = pd.merge(IEA_cleaned_df, population_df, on='region', how='inner')

# Print the merged dataframe to verify
print(IEA_population_merged.head())

# Save the new merged dataframe with population data to an Excel file
IEA_population_merged.to_excel('/Users/kainatshafique/Desktop/F2024/ISI 300/Merged_IEA_BEV_Sales_Population.xlsx', index=False)
