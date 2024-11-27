#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
# Load the Csv file
library_df = pd.read_csv('/mnt/singlefs-4/sandbox_yamidi/QC_Cellecta_data/cellecta_library_211208.csv')

target_site_off_target = library_df['target_site'][library_df['On_target'] == False].tolist()
spacer_off_target = library_df['spacer'][library_df['On_target'] == False].tolist()

#%%
# Define functions
def find_most_similar_with_mismatches(target, smaller_seq):
    max_score = 0
    best_match = ''
    mismatch_positions = []
    
    for i in range(len(target) - len(smaller_seq) + 1):
        score = 0
        current_mismatch_positions = []
        for j, (a, b) in enumerate(zip(target[i:i+len(smaller_seq)], smaller_seq)):
            if a == b:
                score += 1
            else:
                current_mismatch_positions.append(j)
                
        if score > max_score:
            max_score = score
            best_match = target[i:i+len(smaller_seq)]
            mismatch_positions = current_mismatch_positions
    
    return best_match, max_score, mismatch_positions

#%%
# Initialize the matrix and the base pairs excluding matches
base_pairs = ['T:G', 'T:C', 'T:A', 'A:T', 'A:G', 'A:C', 'G:T', 'G:C', 'G:A', 'C:T', 'C:G', 'C:A']
matrix = np.zeros((len(base_pairs), 20))

# Assuming targets_list is your list of target sequences and smaller_seq is defined
targets_list = target_site_off_target  # Replace with your actual list of target sequences
spacer_list = spacer_off_target  # The smaller sequence against which to find matches

for target, spacer in zip(targets_list, spacer_list):
    best_match, max_score, mismatch_positions = find_most_similar_with_mismatches(target, spacer)
    
    # Only proceed if the number of mismatches is 1 or less
    if len(mismatch_positions) <= 1:
        # Fill the matrix based on the best match but exclude matching base pairs
        for i, (base_target, base_smaller) in enumerate(zip(best_match, spacer)):
            if base_target != base_smaller:  # Skip counting if bases are the same
                pair = f"{base_smaller}:{base_target}"
                if pair in base_pairs:
                    matrix[base_pairs.index(pair), i] += 1

# Convert the matrix to a DataFrame for better visualization
df = pd.DataFrame(matrix, index=base_pairs, columns=[f"Pos {i+1}" for i in range(20)])

#%%
# Plot heatmap
sns.set_theme(style="whitegrid")  # Optional: sets the theme for better aesthetics

# Create the heatmap and assign the return value to 'ax' to get the axes object
ax = sns.heatmap(df, annot=False, cmap="Blues")

# Set the y-axis tick labels orientation
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)  # Makes y-axis labels horizontal

plt.title("Target and Spacer Mismatch Plot")
plt.xlabel("Position in Spacer")
plt.ylabel("Base Pair Interactions")
plt.show()

# %%
