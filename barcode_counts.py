# Import Packages:
from Bio import SeqIO
import gzip
from collections import defaultdict
# Function definition:
def barcode_count(file_name,input_dir,barcode_length,output_dir):
    '''
    Counts the occurrences of unique barcodes in a gzipped fastq file.

    This function processes a specified gzipped fastq file to identify and count 
    the occurrences of unique barcode sequences, defined as the first 'barcode_length' 
    bases of each read. The counts are then saved to a CSV file in the specified 
    output directory.

    Parameters:
    - file_name (str): The name of the fastq file (without the '.fastq.gz' extension) to process.
    - input_dir (str): The directory where the gzipped fastq file is located.
    - barcode_length (int): The length of the barcode (number of bases at the start of each read) to consider.
    - output_dir (str): The directory where the output CSV file will be saved. The file is named 
      'barcode_counts_{file_name}.csv', where {file_name} is replaced by the actual name of the 
      input fastq file.

    Output:
    - A CSV file named 'barcode_counts_{file_name}.csv' in the specified output directory. 
      The CSV file contains two columns: 'barcode', which lists each unique barcode sequence, 
      and 'read_count', which lists the corresponding count of each barcode in the fastq file.

    Side Effects:
    - Reads the specified gzipped fastq file from the input directory.
    - Creates and writes to a CSV file in the output directory.
    - Prints a message indicating the completion and output file location.

    Example usage:
    barcode_count("sample", "/path/to/input", 20, "/path/to/output")
    '''
    sequenced_barcodes = defaultdict(int)
    ct = 0
    with gzip.open(f'{input_dir}/{file_name}.fastq.gz', 'rt') as fq:
        for record in SeqIO.parse(fq, 'fastq'):
            ct += 1
            barcode = str(record.seq[:barcode_length])
            sequenced_barcodes[str(record.seq[:barcode_length])] += 1
    # Save number of read per barcode as .csv file:
    with open(f"{output_dir}/barcode_counts_{file_name}.csv", "w") as fout:
        fout.write("barcode,read_count\n")
        for barcode, read_count in sequenced_barcodes.items():
            fout.write(f'{barcode},{read_count}\n')
    print(f"Wrote barcode count to {output_dir}")
