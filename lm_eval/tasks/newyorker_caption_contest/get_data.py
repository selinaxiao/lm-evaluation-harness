import subprocess
import pandas as pd
import json


def fetch_data_and_convert_to_pd(url):
    # Define the curl command
    curl_command = ['curl.exe', '-X', 'GET', url]

    # Execute the curl command and capture the output
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # Check if the curl command was successful
    if result.returncode != 0:
        print("Error fetching data:", result.stderr)
        return

    # Convert the output from JSON to a Python dictionary
    try:
        data_dict = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return

    # Create a list to hold row data
    rows_list = []

    # Iterate through each row in the JSON data
    for row in data_dict['rows']:
        # Each row's data will be stored in a dictionary
        row_data = {}
        # Iterate through each feature, extracting the value from the row
        for feature in data_dict['features']:
            feature_name = feature['name']
            # Check if the feature is a simple value or a nested structure
            if isinstance(row['row'][feature_name], dict):
                # For nested structures like 'image', you might want to flatten it or choose a specific sub-value
                # For example, only extract the 'src' from an image
                if feature_name == 'image':
                    row_data[feature_name] = row['row'][feature_name]['src']
                else:
                    # For other nested structures, join their values or handle as needed
                    row_data[feature_name] = ', '.join(row['row'][feature_name].values())
            elif isinstance(row['row'][feature_name], list):
                # If the value is a list, join it into a single string (or handle as needed)
                row_data[feature_name] = ', '.join(row['row'][feature_name])
                # row_data[feature_name] = row['row'][feature_name]
            else:
                # For simple values, just copy them over
                row_data[feature_name] = row['row'][feature_name]
        # Add the processed row data to our list
        rows_list.append(row_data)

    # Convert the list of row dictionaries into a DataFrame
    df = pd.DataFrame(rows_list)

    return df

    # Display the DataFrame to verify it looks correct
    # print(df.head())

    # df.to_excel(excel_file_path, index=False)

    # print(f"Data successfully saved to {excel_file_path}")


def fetch_batch(config, offset, length=100):
    """Fetch a batch of rows from the API."""
    url = f"https://datasets-server.huggingface.co/rows?dataset=jmhessel%2Fnewyorker_caption_contest&config={config}&split=test&offset={offset}&length={length}"
    df_batch = fetch_data_and_convert_to_pd(url)
    return df_batch


# URL from which to fetch data
# url = "https://datasets-server.huggingface.co/rows?dataset=jmhessel%2Fnewyorker_caption_contest&config=matching&split=test&offset=0&length=100"

# Path for the output Excel file
excel_file_path = 'matching_trial.xlsx'

total_rows = 600
rows_per_request = 100

# Initialize an empty list to store DataFrames
df_list = []

for config in ['matching', 'matching_1', 'matching_2', 'matching_3', 'matching_4']:
    print(config)
    for offset in range(0, total_rows, rows_per_request):
        print(offset)
        df_batch = fetch_batch(config, offset, rows_per_request)
        df_list.append(df_batch)

# Concatenate all DataFrames in the list into a single DataFrame
df_final = pd.concat(df_list, ignore_index=True)

df_final.to_excel(excel_file_path, index=False)

print(f"Data successfully saved to {excel_file_path}")

# Call the function
# fetch_data_and_convert_to_pd(url, excel_file_path)
