import pandas as pd

def load_data(file_path):
    """Load the data from the given file path."""
    try:
        data = pd.read_csv(file_path, low_memory=False)
        print(f"Data loaded successfully from {file_path}.")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")

def merge_datasets(applications_data, permits_data):
    """Merge the Job Application and Permit Issuance datasets based on a common key."""
    try:
        # Strip whitespace from both datasets' column names
        applications_data.columns = applications_data.columns.str.strip()
        permits_data.columns = permits_data.columns.str.strip()

        # Rename 'Job #' in both datasets to 'Job Number' for consistency
        applications_data.rename(columns={'Job #': 'Job Number'}, inplace=True)
        permits_data.rename(columns={'Job #': 'Job Number'}, inplace=True)

        # Merge datasets on the 'Job Number' column
        merged_data = pd.merge(applications_data, permits_data, on='Job Number', how='inner')

        print("Datasets merged successfully.")
        return merged_data
    except Exception as e:
        print(f"Error merging datasets: {e}")
        return None

def filter_data(data, job_type=None, start_date=None, end_date=None):
    """Filter the data based on job type and date range."""
    if 'Job Type' in data.columns:
        # Proceed with filtering by job type if the column exists
        if job_type:
            data = data[data['Job Type'] == job_type]
    else:
        print("Column 'Job Type' not found in the merged dataset.")

    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        if 'Latest Action Date' in data.columns:
            data['Latest Action Date'] = pd.to_datetime(data['Latest Action Date'], errors='coerce')
            data = data[(data['Latest Action Date'] >= start_date) & (data['Latest Action Date'] <= end_date)]
        else:
            print("Column 'Latest Action Date' not found in the dataset.")

    return data

# File paths for the datasets
applications_file_path = 'C:/Users/manae/OneDrive - The City University of New York/Desktop/Fall 2024/ISI 300/project/DOB_Job_Application_Filings_20241009.csv'
permits_file_path = 'C:/Users/manae/OneDrive - The City University of New York/Desktop/Fall 2024/ISI 300/project/DOB_Permit_Issuance_20241022.csv'

# Load the datasets
job_applications = load_data(applications_file_path)
permit_issuance = load_data(permits_file_path)

# Merge the datasets based on 'Job Number'
merged_data = merge_datasets(job_applications, permit_issuance)

# Print merged dataset columns for inspection
if merged_data is not None:
    print("Merged Dataset Columns:", merged_data.columns)

# Filter the merged data for analysis (e.g., job type 'A2', date range Jan 2023)
if merged_data is not None:
    filtered_merged_data = filter_data(merged_data, job_type='A2', start_date='2023-01-01', end_date='2023-01-31')

    # Display the first few rows of the merged and filtered data
    print(filtered_merged_data.head())
else:
    print("Merged data is None. Check for issues with merging.")
