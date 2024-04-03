import os
import datetime

import pandas as pd

import fcntl  # For file locking

def read_pqt_with_lock(file_name):
    """
    Read Parquet file with file-level lock.

    Args:
        file_name (str): Name of the Parquet file to read.

    Returns:
        pandas.DataFrame: DataFrame read from the Parquet file.
    """
    assert file_name.endswith(".pqt"), "File name must end with '.pqt'"
    with open(file_name, 'rb') as file:
        fcntl.flock(file, fcntl.LOCK_SH)  # Use LOCK_SH for shared read access
        df  =   pd.read_parquet(file)
        fcntl.flock(file, fcntl.LOCK_UN)
        print("{0} read in df.shape={1}".format(file_name, df.shape))
    return df

def write_pqt_with_lock(df, file_name):
    """
    Write DataFrame to Parquet file with file-level lock.

    Args:
        df (pandas.DataFrame): DataFrame to write to the Parquet file.
        file_name (str): Name of the Parquet file to write.

    Returns:
        None
    """
    assert file_name.endswith(".pqt"), "File name must end with '.pqt'"
    with open(file_name, 'wb') as file:
        fcntl.flock(file, fcntl.LOCK_SH)  # Use LOCK_SH for shared read access
        df.to_parquet(file)
        fcntl.flock(file, fcntl.LOCK_UN)
        print("{0} writing df.shape={1}".format(file_name, df.shape))
    return df

def combine_dfs(comb_file_name, dir_path, file_types_to_merge):
    """
    Combine dataframes from Parquet files in a directory.

    Args:
        comb_file_name (str): Name of the combined Parquet file.
        dir_path (str): Directory path containing Parquet files.
        file_types_to_merge (list): List of file extensions to merge.

    Returns:
        pandas.DataFrame: Combined dataframe.
    """
    
    files           =   [dir_path+f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    files_pqt       =   [f for f in files if f.endswith('.pqt') and not any(substring in f for substring in ['datapackage.json', '.~lock.'])]
    files_pqt.sort()

    if os.path.isfile(comb_file_name):
        do_comb =   any(datetime.datetime.fromtimestamp(os.path.getctime(file)) >= datetime.datetime.fromtimestamp(os.path.getctime(comb_file_name)) \
                        for file in files_pqt)
        if not do_comb:
            print("comb_file_name={0} already up to date".format(comb_file_name))
            return read_pqt_with_lock(comb_file_name)

    df_full =   pd.concat([read_pqt_with_lock(file) for file in files_pqt], axis=0).sort_index()
    df_full =   df_full.loc[~df_full.index.duplicated(keep='first')]    #   will get occasional overlap of one period
    write_pqt_with_lock(df_full, comb_file_name)
    return df_full