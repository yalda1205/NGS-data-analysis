# Import Packages:
import pandas as pd
import os

#Function definition:
def target_to_fasta(input_dir,file_name,col_number,output_dir):
    '''
    Converts a specified column (target_site/reference) from a CSV file containing DNA sequences into FASTA format files.

    This function reads a CSV file from the specified input directory and column (target_site/reference), then writes each sequence
    to a separate FASTA file in the specified output directory. The name of each FASTA file is derived
    from the 'barcode' column in the CSV file. It ensures the output directory exists, creating it if necessary.

    Parameters:
    - input_dir (str): Directory where the input CSV file is located.
    - file_name (str): Name of the input CSV file (without the .csv extension).
    - col_number (int): Index (0-based) of the column in the CSV file that contains the DNA sequences (target_site/reference).
    - output_dir (str): Directory where the output FASTA files will be saved.

    Outputs:
    - FASTA files for each sequence in the specified column of the CSV file. Each file is named using the
      corresponding value from the 'barcode' column of the CSV file, with a `.fa` extension.
    - Prints a message indicating completion and the directory where the FASTA files are saved.

    Returns:
    - None
    '''
    library_df = pd.read_csv(f'{input_dir}/{file_name}.csv')
    # Directory where you want to save the FASTA files
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each row in the DataFrame
    for index, row in library_df.iterrows():
        # Assuming the sequence is in the col_number
        sequence = row.iloc[col_number]
        # Create a filename based on barcode
        fasta_filename = f'{output_dir}/{library_df.barcode[index]}.fa'
        # Write the sequence to a FASTA file
        with open(fasta_filename, 'w') as fasta_file:
            fasta_file.write(f'>sequence_{index + 1}\n{sequence}')
    print(f'FASTA files have been created in the "{output_dir}" directory.')
