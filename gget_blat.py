#%%

import gget
import glob
import time
import urllib.error
import pandas as pd
from http.client import RemoteDisconnected
#%%
# Load the Csv file
library_df = pd.read_csv('/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/target_extra.csv')
target_site = library_df['target'].tolist()
df = pd.read_csv('/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/cellecta_library_211208.csv')
df_filtered = df[df['target_site'].isin(target_site)]
barcode_list = df_filtered['barcode'].tolist()

data_frames = []
jump_target = []

for target, barcode in zip(target_site, barcode_list):
    fasta = target
    attempt = 0
    success = False
    while attempt < 5 and not success:  # Retry up to 5 times
        try:
            temp_data = gget.blat(fasta)
            if temp_data is None:
                jump_target.append(target)
                attempt += 1
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                temp_data['barcodes'] = barcode
                data_frames.append(temp_data)
                success = True
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.reason}. Retrying...")
            attempt += 1
            time.sleep(2 ** attempt)  # Exponential backoff
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}. Retrying...")
            attempt += 1
            time.sleep(2 ** attempt)
        except RemoteDisconnected:
            print("RemoteDisconnected: Retrying...")
            attempt += 1
            time.sleep(2 ** attempt)

# Concatenate all DataFrames in the list, if any were successfully retrieved
if data_frames:
    data = pd.concat(data_frames, ignore_index=True)
else:
    data = pd.DataFrame()  # or handle the case where no data could be retrieved

data.to_csv("/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/blat_output_6.csv", index=False)
df_target = pd.DataFrame(jump_target,columns=['target'])
df_target.to_csv("/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/target_extra.csv", index=False)

# %%
