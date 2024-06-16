import pandas as pd

# Read the dataset from a text file with the correct delimiter
df = pd.read_csv('output_AGB_dataset.txt', delimiter=',')

# Print the DataFrame to debug and check the column names
print("DataFrame Columns:", df.columns)

# Define the function to calculate CARBON_SEQUESTRATION
def calculate_carbon_sequestration(agb):
    biomass_tot = agb + (agb * 1.2)
    dry_weight = biomass_tot * 0.725
    carbon_storage = dry_weight * 0.5
    carbon_sequestration = carbon_storage * (44 / 12)
    return carbon_sequestration

# Check if 'AGB' column exists in the DataFrame
if 'AGB' in df.columns:
    # Apply the function to the AGB column and create a new column CARBON_SEQUESTRATION
    df['CARBON_SEQUESTRATION'] = df['AGB'].apply(calculate_carbon_sequestration)

    # Select the required columns
    result_df = df[['Id', 'Species', 'Latitude', 'Longitude', 'CARBON_SEQUESTRATION']]

    # Save the results to a new text file with comma delimiter
    result_df.to_csv('carbon_sequestration_dataset.txt', index=False, sep=',')

    print("Results saved to 'carbon_sequestration_dataset.txt'")
else:
    print("Column 'AGB' not found in the DataFrame")
