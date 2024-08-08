# -*- coding: utf-8 -*-
"""OCM_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_gxw-tsWCqkEdkghQxenIdbR4G65N0DB
"""

import pandas as pd
import numpy as np

# Load the CSV file
file_path = '/content/OCMData.csv'
data = pd.read_csv(file_path)

# Function to convert a string with multiple values into a numpy array
def convert_to_array(value):
    if isinstance(value, str) and ',' in value:
        try:
            return np.array(value.split(','), dtype=float)
        except ValueError:
            return value
    return value

# List of columns to convert
columns_to_convert = [
    'Ferrous Particle Bin Upper Endpoints',
    'Ferrous Particle Counts',
    'Nonferrous Particle Bins Upper Endpoints',
    'Nonferrous Particle Counts',
    'Total Ferrous Mass',
    'Total Nonferrous Mass'
]

# Apply the function to relevant columns
for column in columns_to_convert:
    data[column] = data[column].apply(convert_to_array)

# Ensure exponential numbers are stored as large floats
def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return value

data = data.applymap(lambda x: convert_to_float(x) if isinstance(x, str) and 'E' in x else x)



# Display the first few rows of the processed dataframe
print(data)

# Inspect the column names and their data types
data.dtypes

# List of columns to convert
columns_to_convert = [
    'Ferrous Particle Bin Upper Endpoints',
    'Ferrous Particle Counts',
    'Nonferrous Particle Bins Upper Endpoints',
    'Nonferrous Particle Counts',
    'Total Ferrous Mass',
    'Total Nonferrous Mass'
]

# Apply the function to relevant columns
for column in columns_to_convert:
    data[column] = data[column].apply(convert_to_array)

# Ensure exponential numbers are stored as large floats
data = data.applymap(lambda x: float(x) if isinstance(x, str) and 'E' in x else x)

# Save the processed data to a new CSV file
output_file_path = '/content/OCM_Data.csv'
data.to_csv(output_file_path, index=False)

# Display the first few rows of the processed dataframe
data.head()

import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file
csv_file = '/content/OCMData.csv'  # Update this path if needed
df = pd.read_csv(csv_file)

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d,%Y %H:%M:%S %p')

# Initialize the 'Timeleft' column with 60 hours for the first row
initial_timeleft = timedelta(hours=60)
df.loc[0, 'Timeleft'] = initial_timeleft

# Calculate the 'Timeleft' for the remaining rows
for i in range(1, len(df)):
    time_diff = df.loc[i, 'Timestamp'] - df.loc[i - 1, 'Timestamp']
    df.loc[i, 'Timeleft'] = df.loc[i - 1, 'Timeleft'] - time_diff

# Convert 'Timeleft' column to a string format
df['Timeleft'] = df['Timeleft'].apply(lambda x: str(x))

# Save the updated DataFrame to a new CSV file
output_file = 'updated_timeleft.csv'
df.to_csv(output_file, index=False)

print(f"Updated data has been saved to {output_file}")

import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file
file_path = '/content/EntireData_TillBEML_Report_2024_06_06.csv'
df = pd.read_csv(file_path)

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d,%Y %H:%M:%S %p')

# Function to process each segment
def process_segment(df, start_time, initial_duration):
    df = df.sort_values('Timestamp').reset_index(drop=True)

    initial_time = start_time
    duration_left = initial_duration
    time_left = []

    for i in range(len(df)):
        if i == 0:
            elapsed_time = df['Timestamp'][i] - initial_time
        else:
            elapsed_time = df['Timestamp'][i] - df['Timestamp'][i-1]

        duration_left -= elapsed_time
        time_left.append(duration_left)

    df['RUL'] = [str(timedelta(seconds=int(t.total_seconds()))) for t in time_left]
    return df

# Define the segments with start times and durations
segments = [
    ("May 24,2024 14:00:00 PM", timedelta(hours=300)),
    ("May 26,2024 12:05:00 PM", timedelta(hours=300)),
    ("May 27,2024 07:10:00 AM", timedelta(hours=300)),
    ("May 27,2024 10:30:00 AM", timedelta(hours=30)),
    ("May 28,2024 07:15:00 AM", timedelta(hours=30)),
    ("May 29,2024 07:40:00 AM", timedelta(hours=30)),
    ("May 31,2024 10:10:00 AM", timedelta(hours=0)),
    ("May 31,2024 14:00:00 PM", timedelta(hours=0))
]

# Process each segment and concatenate the results
final_df = pd.DataFrame()

for start_time_str, initial_duration in segments:
    start_time = datetime.strptime(start_time_str, '%b %d,%Y %H:%M:%S %p')
    segment_df = df[(df['Timestamp'] >= start_time) & (df['Timestamp'] < (start_time + initial_duration))]
    processed_segment = process_segment(segment_df, start_time, initial_duration)
    final_df = pd.concat([final_df, processed_segment])

# Save the updated DataFrame to a new CSV file
output_file_path = '300hrs_30_0hrs_OCM_data.xlsx'
final_df.to_excel(output_file_path, index=False)

print("Timeleft column added and saved to new CSV file.")

import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file
file_path = '/content/EntireData_TillBEML_Report_2024_06_06.csv'
df = pd.read_csv(file_path)

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d,%Y %H:%M:%S %p')

# Function to format timedelta as hh:mm:ss with hours exceeding 24
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Function to process each segment
def process_segment(df, start_time, initial_duration):
    df = df.sort_values('Timestamp').reset_index(drop=True)

    initial_time = start_time
    duration_left = initial_duration
    time_left = []

    for i in range(len(df)):
        if i == 0:
            elapsed_time = df['Timestamp'][i] - initial_time
        else:
            elapsed_time = df['Timestamp'][i] - df['Timestamp'][i-1]

        duration_left -= elapsed_time
        time_left.append(duration_left)

    df['Timeleft'] = [format_timedelta(t) for t in time_left]
    return df

# Define the segments with start times and durations
segments = [
    ("May 24,2024 14:00:00 PM", timedelta(hours=300)),
    ("May 26,2024 12:05:00 PM", timedelta(hours=300)),
    ("May 27,2024 07:10:00 AM", timedelta(hours=300)),
    ("May 27,2024 10:30:00 AM", timedelta(hours=30)),
    ("May 28,2024 07:15:00 AM", timedelta(hours=30)),
    ("May 29,2024 07:40:00 AM", timedelta(hours=30)),
    ("May 31,2024 10:10:00 AM", timedelta(hours=0)),
    ("May 31,2024 14:00:00 PM", timedelta(hours=0))
]

# Process each segment and concatenate the results
final_df = pd.DataFrame()

for start_time_str, initial_duration in segments:
    start_time = datetime.strptime(start_time_str, '%b %d,%Y %H:%M:%S %p')
    segment_df = df[(df['Timestamp'] >= start_time) & (df['Timestamp'] < (start_time + initial_duration))]
    processed_segment = process_segment(segment_df, start_time, initial_duration)
    final_df = pd.concat([final_df, processed_segment])

# Save the updated DataFrame to a new CSV file
output_file_path = '300h_30h_0h_OCM_Timeleft.csv'
final_df.to_csv(output_file_path, index=False)

print("Timeleft column added and saved to new CSV file.")

import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file
file_path = '/content/EntireData_TillBEML_Report_2024_06_06.csv'
df = pd.read_csv(file_path)

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d,%Y %H:%M:%S %p')

# Function to format timedelta as hh:mm:ss with hours exceeding 24
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Function to process each segment
def process_segment(df, start_time, initial_duration):
    df = df.sort_values('Timestamp').reset_index(drop=True)

    initial_time = start_time
    duration_left = initial_duration
    time_left = []

    for i in range(len(df)):
        if i == 0:
            elapsed_time = df['Timestamp'][i] - initial_time
        else:
            elapsed_time = df['Timestamp'][i] - df['Timestamp'][i-1]

        duration_left -= elapsed_time
        time_left.append(duration_left)

    df['RUL'] = [format_timedelta(t) for t in time_left]
    return df

# Define the segments with start times and durations
segments = [
    ("May 24,2024 14:00:00 PM", timedelta(hours=300)),
    ("May 26,2024 12:05:00 PM", timedelta(hours=300)),
    ("May 27,2024 07:10:00 AM", timedelta(hours=300)),
    ("May 27,2024 10:30:00 AM", timedelta(hours=30)),
    ("May 28,2024 07:15:00 AM", timedelta(hours=30)),
    ("May 29,2024 07:40:00 AM", timedelta(hours=30)),
    ("May 31,2024 10:10:00 AM", timedelta(hours=0)),
    ("May 31,2024 14:00:00 PM", timedelta(hours=0))
]

# Process each segment and concatenate the results
final_df = pd.DataFrame()

for start_time_str, initial_duration in segments:
    start_time = datetime.strptime(start_time_str, '%b %d,%Y %H:%M:%S %p')
    segment_df = df[(df['Timestamp'] >= start_time) & (df['Timestamp'] < (start_time + initial_duration))]
    processed_segment = process_segment(segment_df, start_time, initial_duration)
    final_df = pd.concat([final_df, processed_segment])

# Save the updated DataFrame to a new CSV file
output_file_path = '300hrs_30_0hrs_OCM_data.csv'
final_df.to_csv(output_file_path, index=False)

print("Timeleft column added and saved to new CSV file.")

import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file
file_path = '/content/EntireData_TillBEML_Report_2024_06_06.csv'
df = pd.read_csv(file_path)

# Convert the 'Timestamp' column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d,%Y %H:%M:%S %p')

# Function to format timedelta as hh:mm:ss with hours exceeding 24
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(abs(total_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    sign = '-' if td.total_seconds() < 0 else ''
    return f"{sign}{hours:02}:{minutes:02}:{seconds:02}"

# Function to process each segment
def process_segment(df, start_time, initial_duration):
    df = df.sort_values('Timestamp').reset_index(drop=True)

    initial_time = start_time
    duration_left = initial_duration
    time_left = []

    for i in range(len(df)):
        if i == 0:
            elapsed_time = df['Timestamp'][i] - initial_time
        else:
            elapsed_time = df['Timestamp'][i] - df['Timestamp'][i-1]

        duration_left -= elapsed_time
        time_left.append(duration_left)

    df['RUL'] = [format_timedelta(t) for t in time_left]
    return df

# Define the segments with start times and durations
segments = [
    ("May 24,2024 14:00:00 PM", timedelta(hours=300)),
    ("May 26,2024 12:05:00 PM", timedelta(hours=300)),
    ("May 27,2024 07:10:00 AM", timedelta(hours=300)),
    ("May 27,2024 10:30:00 AM", timedelta(hours=30)),
    ("May 28,2024 07:15:00 AM", timedelta(hours=30)),
    ("May 29,2024 07:40:00 AM", timedelta(hours=30)),
    ("May 31,2024 10:10:00 AM", timedelta(hours=0)),
    ("May 31,2024 14:00:00 PM", timedelta(hours=0))
]

# Process each segment and concatenate the results
final_df = pd.DataFrame()

for start_time_str, initial_duration in segments:
    start_time = datetime.strptime(start_time_str, '%b %d,%Y %H:%M:%S %p')
    if initial_duration == timedelta(hours=0):
        # Select timestamps for one day after the start time for zero duration segments
        segment_df = df[(df['Timestamp'] >= start_time) & (df['Timestamp'] < start_time + timedelta(days=1))]
    else:
        segment_df = df[(df['Timestamp'] >= start_time) & (df['Timestamp'] < start_time + initial_duration)]
    processed_segment = process_segment(segment_df, start_time, initial_duration)
    final_df = pd.concat([final_df, processed_segment])

# Save the updated DataFrame to a new CSV file
output_file_path = 'OCM_300h_30h_0h_Timeleft.csv'
final_df.to_csv(output_file_path, index=False)

print("Timeleft column added and saved to new CSV file.")

import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file into a pandas DataFrame
file_path = '/content/EntireData_TillBEML_Report_2024_06_06.csv'
df = pd.read_csv(file_path)

# Define the segment details
segments = [
    {"start": "May 24,2024 14:00:00 PM", "end": "May 24,2024 17:02:00 PM", "hours": 300},
    {"start": "May 26,2024 12:05:00 PM", "end": "May 26,2024 15:20:00 PM", "hours": 300},
    {"start": "May 27,2024 07:10:00 AM", "end": "May 27,2024 10:10:00 AM", "hours": 300},
    {"start": "May 27,2024 10:30:00 AM", "end": "May 27,2024 13:34:00 PM", "hours": 30},
    {"start": "May 27,2024 14:10:00 PM", "end": "May 27,2024 17:00:00 PM", "hours": 30},
    {"start": "May 28,2024 07:15:00 AM", "end": "May 28,2024 10:15:00 AM", "hours": 30},
    {"start": "May 29,2024 07:40:00 AM", "end": "May 29,2024 10:20:00 AM", "hours": 30},
    {"start": "May 31,2024 10:10:00 AM", "end": "May 31,2024 13:10:00 PM", "hours": 0},
    {"start": "May 31,2024 14:00:00 PM", "end": "May 31,2024 16:35:00 PM", "hours": 0},
]

# Convert Timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%b %d,%Y %H:%M:%S %p')


# Function to calculate Timeleft
def calculate_timeleft(df, start_time, end_time, initial_hours):
    segment_df = df[(df['Timestamp'] >= start_time) & (df['Timestamp'] <= end_time)].copy()
    segment_df['RUL'] = initial_hours * 3600  # Convert hours to seconds
    previous_time = start_time

    for i, row in segment_df.iterrows():
        current_time = row['Timestamp']
        time_diff = (current_time - previous_time).total_seconds()
        segment_df.at[i, 'RUL'] -= time_diff
        previous_time = current_time

    # Convert Timeleft from seconds to H:M:S format
    def format_timeleft(seconds):
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    segment_df['RUL'] = segment_df['RUL'].apply(format_timeleft)

    return segment_df

# Process each segment
result_df = pd.DataFrame()
for segment in segments:
    start_time = datetime.strptime(segment['start'], '%b %d,%Y %H:%M:%S %p')
    end_time = datetime.strptime(segment['end'], '%b %d,%Y %H:%M:%S %p')
    segment_df = calculate_timeleft(df, start_time, end_time, segment['hours'])
    result_df = pd.concat([result_df, segment_df])

# Save the result to a new CSV file
output_file_path = 'OCM_Timeleft_300h_30h_0h.csv'
result_df.to_csv(output_file_path, index=False)
print("Timeleft column added and saved to new CSV file.")

import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = '/content/OCM_Timeleft_300h_30h_0h.csv'
df = pd.read_csv(file_path)

# Split the 'Ferrous Particle Bins Upper Endpoints' into separate columns
ferrous_split = df['Ferrous Particle Bin Upper Endpoints'].str.split(',', expand=True)
ferrous_split.columns = [f'FP{i+1}' for i in range(ferrous_split.shape[1])]

# Split the 'Ferrous Particle Counts' into separate columns
ferrous_count_split = df['Ferrous Particle Counts'].str.split(',', expand=True)
ferrous_count_split.columns = [f'FPC{i+1}' for i in range(ferrous_count_split.shape[1])]

# Split the 'Nonferrous Particle Bins Upper Endpoints' into separate columns
nonferrous_split = df['Nonferrous Particle Bins Upper Endpoints'].str.split(',', expand=True)
nonferrous_split.columns = [f'NFP{i+1}' for i in range(nonferrous_split.shape[1])]

# Split the 'Nonferrous Particle Counts' into separate columns
nonferrous_count_split = df['Nonferrous Particle Counts'].str.split(',', expand=True)
nonferrous_count_split.columns = [f'NFPC{i+1}' for i in range(nonferrous_count_split.shape[1])]

# Concatenate the new columns to the original DataFrame
df = pd.concat([df, ferrous_split, ferrous_count_split , nonferrous_split,nonferrous_count_split ], axis=1)

# Save the result to a new CSV file
output_file_path = 'Cleaned_OCM_Timeleft_300h_30h_0h.csv'
df.to_csv(output_file_path, index=False)
print("Data cleaning complete and saved to new CSV file.")
df.head()
df.tail()

import pandas as pd

# Load the CSV file
file_path = '/content/EntireData_TillBEML_Report_2024_06_06.csv'
df = pd.read_csv(file_path)

# Initialize an empty list to store the new rows
new_rows = []

# Counter for NPF numbering
npf_counter = 1

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Split the values in the "Nonferrous Particle Counts" column by comma
    particle_counts = str(row['Nonferrous Particle Counts']).split(',')

    # Iterate through each particle count and create new rows
    for count in particle_counts:
        if count.strip() == '0':
            new_row = row.copy()
            new_row['Nonferrous Particle Counts'] = f"0 - NPF{npf_counter}"
            new_rows.append(new_row)
            npf_counter += 1

# Create a new DataFrame from the new rows
new_df = pd.DataFrame(new_rows)

# Save the cleaned DataFrame to a new CSV file
output_file_path = 'Cleaned_Data_with_Nonferrous_Particle_Counts.csv'
new_df.to_csv(output_file_path, index=False)

print("Data cleaning complete and saved to new CSV file.")