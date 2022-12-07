###Data Imports
import os
import numpy as np
import pandas as pd

###Pandas options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Get files from designated directory
def get_file_data(PATH) -> str:
    assert type(PATH) == str
    
    #Return file metadata
    def get_stats(target_path) -> list:
        #Converts weird timestamp to ISO timestamp string
        def convert_datetime(timestamp_string):
            from datetime import datetime, timezone
            result = datetime.fromtimestamp(timestamp_string, tz=timezone.utc)
            dt_string = str(result.year) + '-' + str(result.month) + '-' + str(result.day) + ' ' + str(result.time())
            return dt_string

        def convert_bytes(file_size):
            if file_size < 1024:
                final_size = file_size
                unit = 'B'
            elif file_size >= 1024 and file_size < 1024**2:
                final_size = file_size / 1024
                unit = 'KB'
            elif file_size >= 1024**2 and file_size < 1024**3:
                final_size = file_size / 1024**2
                unit = 'MB'
            elif file_size >= 1024**3 and file_size < 1024**4:
                final_size = file_size / 1024**3
                unit = 'GB'
            else:
                pass

            return [final_size, unit]

        final_out = []

        for file in target_path:
            stats = os.stat(file)
            created = convert_datetime(stats.st_ctime)
            modified = convert_datetime(stats.st_mtime)
            final_size = convert_bytes(stats.st_size)
            dates = [created, modified]
            dates.extend(final_size)
            final_out.append(dates)

        df_final = pd.DataFrame(final_out, columns=['Created', 'Modified', 'Size', 'Unit'])

        return df_final

    #Empty List to hold path info
    df = []

    #Scan directory and store path and file info
    for i in os.walk(PATH, topdown=True):
        df.append([i[0], i[-1]])

    #Convert list to DataFrame
    new_df = pd.DataFrame(df, columns=['Path', 'Files'])

    #Parse information 
    new_file_list = []
    for idx in new_df.index.tolist():
        for file in new_df.Files[idx]:
            extension = file.split('.')[-1].lower()
            full_path = new_df.Path[idx]+'\\'+file
            new_file_list.append([full_path, new_df.Path[idx], file.lower(), extension]) #Make all filenames lower to bypass case-sensitivity

    df_files = pd.DataFrame(new_file_list, columns=['Full_Path', 'Path', 'File', 'Ext']) #Label file info
    df_final = get_stats(df_files.Full_Path) #Get file metadata
    df_final = pd.concat([df_files, df_final], axis=1) #Concatenate file metadata to file info

    return df_final
    
def find_duplicates(dataframe):
    #Slice to file and extension
    df1 = dataframe.loc[:, ['File', 'Ext']].groupby(['File']).count()
    df1.reset_index(inplace=True, drop=False)
    
    #Filter by filename
    dupes = df1[df1.Ext > 1]
    dupes.columns = ['File', 'Count']
    data2 = pd.merge(dataframe, dupes, how='left', left_on='File', right_on='File')
    data2.fillna(value=1, inplace=True)
    data2.Count = data2.Count.astype(int)
    
    #Filter by filesize
    dupes_2 = data2[data2.Count > 1].loc[:, ['File', 'Modified', 'Size']]
    dupes_3 = dupes_2.groupby(['File', 'Size']).count()
    dupes_3.reset_index(inplace=True, drop=False)
    dupes_4 = dupes_3.loc[:, ['File', 'Modified']]
    dupes_4.columns = ['File', 'Ct_2']
    dupes_5 = dupes_4[dupes_4.Ct_2 > 1]
    data3 = pd.merge(data2, dupes_5, how='left', left_on='File', right_on='File')
    data3.fillna(value=1, inplace=True)
    data3.Ct_2 = data3.Ct_2.astype(int)
    
    
    return data3

#Compare left and right tables for duplicates and unique files
def unique_in_rt_table(DF_LEFT, DF_RIGHT):
    #Add ids to be able to sort later
    DF_LEFT['Table_ID'] = 'Main'
    DF_RIGHT['Table_ID'] = 'Comp'
    
    assert DF_LEFT.columns.tolist() == DF_RIGHT.columns.tolist()
    
    both_tables = pd.concat([DF_LEFT, DF_RIGHT.loc[:, DF_LEFT.columns.tolist()]])
    
    #Separate unique files
    bt_w_dupes = find_duplicates(both_tables)
    unique_files = bt_w_dupes[bt_w_dupes.Ct_2 == 1]
    unique_final = unique_files[unique_files.Table_ID == 'Comp']
    
    #Separate duplicates
    only_dupes = bt_w_dupes[bt_w_dupes.Ct_2 > 1].copy()
    only_dupes['Duplicate_Directories'] = [[] for i in range(0, len(only_dupes))] #Add empty list to append duplicate file directories into

    #Add id columns for duplicate tables
    main_dupes = only_dupes[only_dupes.Table_ID == 'Main'] 
    comp_dupes = only_dupes[only_dupes.Table_ID == 'Comp']
    main_dupes.reset_index(inplace=True, drop=True)
    comp_dupes.reset_index(inplace=True, drop=True)

    #Annotate locations of duplicate files
    for idx in comp_dupes.index.tolist():
        for main_idx in main_dupes.index.tolist():
            if comp_dupes.File[idx] == main_dupes.File[main_idx] and comp_dupes.Size[idx] == main_dupes.Size[main_idx]: #Check file name and file size
                main_dupes.Duplicate_Directories[main_idx].append(comp_dupes.Path[idx]) #Add location of duplicate file to main file
            else:
                pass
    
    main_dupes['DDL'] = [len(i) for i in main_dupes.Duplicate_Directories]
    duplicate_final = main_dupes.query('DDL > 0').copy()
            
    return unique_final, duplicate_final


