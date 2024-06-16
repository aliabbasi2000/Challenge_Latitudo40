import pandas as pd
import numpy as np

# Read the data from the text file
file_path = 'input_DBH_dataset.txt'
df = pd.read_csv(file_path)

# Strip any whitespace from the column names
df.columns = df.columns.str.strip()

# Function to calculate AGB based on the tree type and allometric equations
def calculate_agb(row):
    DBH = row['DBH']
    #H = row['Height']
    tree_type = row['Species'].strip()
    
    # for the horse chestnut tree we use an average valuse between two alometric equations
    if tree_type == 'Horse Chestnut':
        log_biomass = 1.8096 + 0.6836 * np.log10(DBH)
        AGB = 10 ** log_biomass

    #elif tree_type == 'Beech':
        #We exlcude it because it has Height parameter
        #AGB = -5.5632 + 0.03008*(DBH) ** 2 *H + 0.1546*(DBH) ** 2

    elif tree_type == 'European Nettle Tree':   
        log_volume = -1.929 + 2.335 * np.log10(DBH)
        AGB = 10 ** log_volume

    elif tree_type == 'European Red Pine':
        AGB = 2.6374 + 0.04102 * (DBH ** 2) * 2.2
        #AGB = 2.6374 + 0.04102 * (DBH ** 2) * H
        
    else:
        AGB = np.nan  # If tree type is not recognized, return NaN

    return AGB

# Apply the AGB calculation to each row
df['AGB'] = df.apply(calculate_agb, axis=1)

# Select the columns for the output
output_df = df[['Id', 'Species', 'Latitude', 'Longitude', 'AGB']]

# Write the output to a new text file
output_file_path = 'output_AGB_dataset.txt'
output_df.to_csv(output_file_path, index=False)
