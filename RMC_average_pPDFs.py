import pandas as pd
import numpy as np
import os
import glob
import shutil

# This script assumes that the script is being run from a folder containing all of the run subfolders and the subfolders begin with the word "run"

# count the number of run folders in current directory *************************************
run_folders = 0
for item in os.listdir(os.curdir):
	if item.startswith('run') == True and os.path.isdir(item) == True:
		run_folders += 1
		sub_dir = os.path.join(os.curdir, item) # path for subfolder (i.e., run folder)
		
print('***** there are {} run folders'.format(run_folders))
		
# determine the number of pPDFs (i.e., columns in CSV file) ********************************
atom_n = int(input('How many atom types are there?: '))

n_pPDFs = atom_n
add_value = atom_n - 1
while add_value > 0:
	n_pPDFs = n_pPDFs + add_value
	add_value = add_value - 1

print('***** there are {} partial PDFs'.format(n_pPDFs))

# create DataFrame for of all .csv files in all run folders ********************************
run_n = 1
path_list = [] # list of paths for each *_PDFpartials.csv file

while run_n <= run_folders:
	run_dir = os.path.join(os.curdir, 'run_{}'.format(run_n)) # setting path for run folder
	if run_n == 1:
		for file in [f for f in os.listdir(run_dir) if f.endswith('.rmc6f')]:
			stem_name, rmc6f_ext = os.path.splitext(file) # setting stem_name equal to basename of .rmc6f file
	CSV_path = os.path.join(run_dir, '{}_PDFpartials.csv'.format(stem_name))
	path_list.append(CSV_path) # populating path_list
	run_n += 1

name_list = ['df_' + str(i) for i in range(1, run_folders+1)] # list of DataFrame names

dataDct = {} # making dictionary where each key is a DF name and the corresponding value is the DF/csv data
for k, v in zip(name_list, path_list):
	dataDct[k] = pd.read_csv(v)

# define function for calculating pPDF value averaged over all runs ************************
def calc_avg(index_val, col_val, runs):
	numerator = 0
	for i in range(1, runs+1):
		numerator += dataDct['df_{}'.format(i)].get_value(index_val, dataDct['df_{}'.format(i)].columns[col_val])
	return numerator/runs
	
# calculate average pPDFs ******************************************************************
columns = ['pPDF_' + str(i) for i in range(1, n_pPDFs + 1)] # list of column names for output file
columns.insert(0, 'r') # don't forget the r values column!
index = range(dataDct['df_1'].index.size) # list of index values for output file
df_AVG = pd.DataFrame(columns = columns, index = index) # make empty pandas DataFrame

for x in index: # populate output new DataFrame with average pPDFs
	for y in range(n_pPDFs+1):
		col_n = columns[y]
		df_AVG.set_value(x, col_n, calc_avg(x, y, run_folders))

# save new DataFrame to .csv file **********************************************************
df_AVG.to_csv('{}_AVG_{}runs_PDFpartials.csv'.format(stem_name, run_folders), index=False)
		
