#%%
# Load Packages
import pandas as pd
import os

#%%
# Load the Csv file
library_df = pd.read_csv('/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/cellecta_library_211208.csv')
# Directory where you want to save the FASTA files
output_dir = '/indelphi/fastqs/fastp_filtered_fastqs/fasta_files_target_site'
os.makedirs(output_dir, exist_ok=True)

#%%
# Iterate through each row in the DataFrame
for index, row in library_df.iterrows():
    # Assuming the sequence is in the second column, adjust the index as needed
    sequence = row.iloc[6]
    # Create a filename based on the row number or any other unique identifier
    fasta_filename = f'{output_dir}/{library_df.barcode[index]}.fa'
    
    # Write the sequence to a FASTA file
    with open(fasta_filename, 'w') as fasta_file:
        fasta_file.write(f'>sequence_{index + 1}\n{sequence}')

print(f'FASTA files have been created in the "{output_dir}" directory.')
