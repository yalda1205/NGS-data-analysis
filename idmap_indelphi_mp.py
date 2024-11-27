#Import useful packages
import argparse
import itertools
import multiprocessing as mp
import os
import pandas as pd
import subprocess


def run_idmap(fastq_file, out_dir, library_file):
    library_df = pd.read_csv(library_file)
    file_name = os.path.basename(fastq_file)
    sample_name = file_name.split("_trimmed.fastq.gz")[0]
    row_index = library_df.index[library_df['barcode'] == sample_name][0]
    reference = library_df['target_site'][row_index]
    filename1 = fastq_file
    cmd = [ 
        "python", "-m", "scripts.indel_tools.generate_idmap",
        "--filename1", filename1,
        "--samplename", sample_name,
        "--reference", reference,  
        "--reference_name", sample_name,
        "--out_dir", out_dir
        ]
    result = subprocess.run(cmd, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fastq_files", required=True, type=str)
    parser.add_argument("--out_dirs", required=True, type=str)
    parser.add_argument("--library_file", required=True, type=str)
    parser.add_argument("--n_threads", default=mp.cpu_count(), type=int)
    args = parser.parse_args()

    list_of_fastqs = args.fastq_files.split(",")
    out_dirs = args.out_dirs.split(",")
    library_file_repeat = itertools.repeat(args.library_file, len(list_of_fastqs))
    pars = zip(list_of_fastqs, out_dirs, library_file_repeat)
    [os.makedirs(out_dir, exist_ok=True) for out_dir in out_dirs]
    with mp.Pool(args.n_threads) as p:
        p.starmap(run_idmap, pars)

if __name__ == "__main__":
    main()
