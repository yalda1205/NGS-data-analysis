#%% Import packages:
import glob
import pandas as pd 
import os
from scripts.indelphi_scripts.split_fastq_by_barcode import split_fastq_by_barcode as sfb
#%% Read the FASTQ files and make a directory to save the splitted fastqs:
list_of_fastqs = glob.glob("/indelphi/fastqs/fastp_filtered_fastqs/*.fastq.gz")
os.makedirs("/indelphi/fastqs/fastp_filtered_fastqs/fastqs_splitted",exist_ok = True)
#%% Load Cellecta library and extract the barcodes:
library_df = pd.read_csv('/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/cellecta_library_211208.csv')
library_barcodes = library_df['barcode'].values.tolist()
#%% Run the "split_fastq_by_barcode" function:
for idx in range(0,len(list_of_fastqs)):
    file_name = os.path.basename(list_of_fastqs[idx][:-18])
    print (file_name)
    output_dir = f"/indelphi/fastqs/fastp_filtered_fastqs/fastqs_splitted/{file_name}"
    sfb.split_fastq_by_barcode(list_of_fastqs[idx], output_dir)