#%%
#Import useful packages
import subprocess
import os
import glob
import pandas as pd
#%%
#Load the csv file (library refrence)
library_df = pd.read_csv('/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/cellecta_library_211208.csv')
barcode_on_target = library_df['barcode'][library_df['PAM_Check'] == 'FORMAT_MATCH'].tolist()
#%%
#Define the base path for simplicity in formatting the command later
base_path   = "/indelphi/fastqs/fastp_filtered_fastqs/fastqs_splitted"
list_of_dir = os.listdir(base_path)
#%%
#Main Loop
for idx in range(0,len(list_of_dir)):
    list_of_fastqs = glob.glob(f"{base_path}/{list_of_dir[idx]}/fastqs_trimmed/*.fastq.gz")
    out_dir = f"/indelphi/fastqs/fastp_filtered_fastqs/fastqs_splitted/{list_of_dir[idx]}/tmp1"
    out_dir_csv = f"/indelphi/fastqs/fastp_filtered_fastqs/fastqs_splitted/{list_of_dir[idx]}"
    os.makedirs(out_dir_csv, exist_ok=True)
    for j in range(0,len(list_of_fastqs)):
        # The constant parts of your command
        file_name = os.path.basename(list_of_fastqs[j])
        sample_name = file_name.split("_trimmed.fastq.gz")[0]
        if sample_name in barcode_on_target:
            row_index = library_df.index[library_df['barcode'] == sample_name][0]
            reference = library_df['target_site'][row_index]
            filename1 = list_of_fastqs[j]
            cmd = [ 
                "python", "-m", "scripts.indel_tools.generate_idmap",
                "--filename1", filename1,
                "--samplename", sample_name,
                "--reference", reference,  
                "--reference_name", sample_name,
                "--out_dir", out_dir
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
    
    #file_pattern = f"{out_dir}/*_summary.csv"
    #file_list = glob.glob(file_pattern)

    # Read each CSV file into a DataFrame and store them in a list
    #dfs = [pd.read_csv(file) for file in file_list]

    # Concatenate all DataFrames in the list into a single DataFrame
    #tmp_df = pd.concat(dfs, ignore_index=True)
    #print(f"Write the .csv {list_of_dir[idx]}")
    #tmp_df.to_csv(f"{out_dir_csv}/{list_of_dir[idx]}.csv", index=False)

# %%
