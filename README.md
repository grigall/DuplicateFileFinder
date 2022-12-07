# Duplicate File Finder (DFF)
This utility is for finding duplicate files between two different directories. It identifies:
- Duplicates within Main and Comparison directories
- Duplicates between both directories
- Unique files in the Comparison directory

# Technologies
- CSS for styling
- QtGridLayout for layout
- pandas for Data Analysis
- Qt, os, and pandas for file handling

# Logic
The sorting algorithm first compares file names (not-case sensitive), then file sizes to determine the maximum probability of the files being duplicates. Then, it lists the locations of all duplicate files in the Comparison directory with respect to the Main directory.