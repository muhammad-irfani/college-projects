#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#read CSV file into pandas dataframe
IEA_df = pd.read_csv('/Users/muhammadirfani/Desktop/F2024/ISI 300/IEA Global EV Data 2024.csv')

#filter out rows with unit of "percent"
IEA_df = IEA_df[IEA_df.unit != 'percent']

#filter out rows with every region except USA, China, Germany, UK, France, Norway, Iceland, United Kingdom, Netherlands
IEA_df = IEA_df[IEA_df.region.isin(['USA', 'China', 'Germany', 'United Kingdom', 'France', 'Norway', 'Iceland', 'United Kingdom', 'Netherlands'])]

#read exel file into pandas dataframe
Sales_Brand_df = pd.read_excel('/Users/gracecostello/Desktop/F2024/ISI 300/EV_Sales_By_Brand.xlsx')

#read exel file into pandas dataframe & print different sheets from same excel file
df_PHEV = pd.read_excel('/Users/gracecostello/Desktop/F2024/ISI 300/Global_Data_EV.xlsx', sheet_name='PHEV')
#read exel file into pandas dataframe & print different sheets from same excel file
df_BEV = pd.read_excel('/Users/gracecostello/Desktop/F2024/ISI 300/Global_Data_EV.xlsx', sheet_name='BEV')
#read exel file into pandas dataframe & print different sheets from same excel file
df_NCS = pd.read_excel('/Users/gracecostello/Desktop/F2024/ISI 300/Global_Data_EV.xlsx', sheet_name='New Cars Sold')

#eliminate data with years other than 2010 or 2023 in IEA_df
IEA_df = IEA_df[IEA_df.year.isin([2010, 2023])]

#eliminate collumn "mode" in IEA_df
IEA_df = IEA_df.drop(columns=['mode'])

#combine rows if they contain the same region, category, parameter powertrain year unit and add up their value column
IEA_df = IEA_df.groupby(['region', 'category', 'parameter', 'powertrain', 'year', 'unit']).sum().reset_index()

#remove rows with parameter "EV charging points" in IEA_df
IEA_df = IEA_df[IEA_df.parameter != 'EV charging points']

#if the region, category, parameter, powertrain, and unit is the same, add a colums showing the difference in value between 2010 and 2023
IEA_df = IEA_df.pivot_table(index=['region', 'category', 'parameter', 'powertrain', 'unit'], columns='year', values='value', fill_value=0).reset_index()
IEA_df['value difference'] = IEA_df[2023] - IEA_df[2010]
#remove all rows without parameter "EV Sales" in IEA_df
IEA_df = IEA_df[IEA_df.parameter == 'EV sales']
#remove all rows with category other than "Historical" in IEA_df
IEA_df = IEA_df[IEA_df.category == 'Historical']

#save previous query as excel file to desktop
IEA_df.to_excel('/Users/gracecostello/Desktop/F2024/ISI 300/IEA_EV_Sales_2010_2023.xlsx', index=False)

#input IEA_EV_Sales_2010_2023.xlsx into pandas dataframe
IEA_cleaned_df = pd.read_excel('/Users/gracecostello/Desktop/F2024/ISI 300/IEA_EV_Sales_2010_2023.xlsx')

#remove all rows with powertrain other than BEV in IEA_cleaned_df
IEA_cleaned_df = IEA_cleaned_df[IEA_cleaned_df.powertrain == 'BEV']


#change Country/area to region in bev_df
df_BEV = df_BEV.rename(columns={'Country/area': 'region'})
#change any row with region = "United States" to "USA"
df_BEV.loc[df_BEV.region == 'United States', 'region'] = 'USA'
#merge IEA_cleaned_df and df_BEV on region
merged_df = pd.merge(IEA_cleaned_df, df_BEV, on='region', how='inner')
#change row 2010_x to "2010 EV Total" and 2023_x to "2023 EV Total"
merged_df = merged_df.rename(columns={'2010_x': '2010 EV Total', '2023_x': '2023 EV Total'})

#change 2010_y to "2010 EV%" and 2023_y to "2023 EV%"
merged_df = merged_df.rename(columns={'2010_y': '2010 EV%', '2023_y': '2023 EV%'})

#save merged_df as excel file to desktop
merged_df.to_excel('/Users/gracecostello/Desktop/F2024/ISI 300/Merged_IEA_BEV_Sales.xlsx', index=False)
#input new csv file into pandas dataframe
population_df = pd.read_csv('/Users/gracecostello/Desktop/F2024/ISI 300/world_population.csv')

#change the column name "Country/Territory" to "region"
population_df = population_df.rename(columns={'Country/Territory': 'region'})
#change any row with region = "United States" to "USA"
population_df.loc[population_df.region == 'United States', 'region'] = 'USA'
#remove all rows with region other than USA, China, France, Germany, Iceland, Netherlands, Norway, United Kingdom
population_df = population_df[population_df.region.isin(['USA', 'China', 'France', 'Germany', 'Iceland', 'Netherlands', 'Norway', 'United Kingdom'])]

#remove all columns except region, 2022 Population, 2010 Population
population_df = population_df[['region', '2022 Population', '2010 Population']]

#add column showing the percent of change in population between 2010 and 2022
population_df['Population Change'] = (population_df['2022 Population'] - population_df['2010 Population']) / population_df['2010 Population']

#merge population_df and merged_df on region
final_df = pd.merge(population_df, merged_df, on='region', how='inner')
#save final_df as excel file to desktop
final_df.to_excel('/Users/gracecostello/Desktop/F2024/ISI 300/Final_Merged_Data.xlsx', index=False)
print(final_df)

#create a bar graph showing the 2010 EV Total and 2023 EV Total for each region
final_df.plot(x='region', y=['2010 EV Total', '2023 EV Total'], kind='bar')
plt.title('2010 EV Total and 2023 EV Total for Each Region')
#add value lables to the graph
for i in range(len(final_df)):
    plt.text(i, final_df['2010 EV Total'][i], final_df['2010 EV Total'][i], ha='right')
    plt.text(i, final_df['2023 EV Total'][i], final_df['2023 EV Total'][i], ha='left')
#create a bar graph showing the 2010 EV% and 2023 EV% for each region
final_df.plot(x='region', y=['2010 EV%', '2023 EV%'], kind='bar')
plt.title('2010 EV% and 2023 EV% for Each Region')
#add value lables to the graph
for i in range(len(final_df)):
    plt.text(i, final_df['2010 EV%'][i], final_df['2010 EV%'][i], ha='right')
    plt.text(i, final_df['2023 EV%'][i], final_df['2023 EV%'][i], ha='left')
#create a bar graph showing the 2010 Population and 2022 Population for each region
final_df.plot(x='region', y=['2010 Population', '2022 Population'], kind='bar')
plt.title('2010 Population and 2022 Population for Each Region')
#add value lables to the graph
for i in range(len(final_df)):
    plt.text(i, final_df['2010 Population'][i], final_df['2010 Population'][i], ha='right')
    plt.text(i, final_df['2022 Population'][i], final_df['2022 Population'][i], ha='left')
#how to view the graphs
plt.show()
#create treemap showing 2023 EV% for each region
final_df.plot(x='region', y='2023 EV%', kind='pie')
plt.title('2023 EV% for Each Region')
#label the pie chart
plt.legend(final_df['region'], loc='upper right')
#how to view the graph
plt.show()


