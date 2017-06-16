#!/usr/bin/env python3
# coding: utf-8

# In[115]:

import Bio
import pandas as pd
import numpy as np
from Bio.Seq import Seq
from Bio import SeqIO
import os, fnmatch

#insert folder name saved in same directory
print("\n----------------------\n* Welcome to Sarah's FASTQ program *\nThis script will find all fastq files within a folder path.\nIt will then calculate the number of occurances of each squence over 30nt long.\nThe files and squence information are then saved to a csv within the script's folder.\n\nThe csv includes:\nFile Name, File Path, Total Number of Squences, Number of Sequences above 30nt,\nPercent of Sequences over 30nt\n-----------------------\n")


user_input = input("folder path please: ")
folder_path = os.path.abspath(user_input)

result = []
names = []

#search through directory and return files names and paths
def find(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
                names.append(name)

    #return result, names
    file_names = names
find('*.fastq', folder_path)

df = pd.DataFrame({'Names': names,'Path': result})

#iterate over records and find seq over 30nt long
#return total number of seq
#return total number of seq over 30nt
sum_counts = []
record_len = []
for i in range(len(df.index)):
    records = list(SeqIO.parse(df['Path'][i], "fastq"))
    count = 0
    length = []
    for i in range(len(records)):
        length.append(len(records[i].seq))
    for i in range(len(length)):
        #print(length[i])
        if length[i] > 30:
            count = count + 1
    sum_counts.append(count)
    record_len.append(len(records))

#Add information to dataframe
df['Total'] = record_len
df['Above_30_nt'] = sum_counts

#calculate percent of reads over 30nt long
df['Percent_over_30'] = (df['Above_30_nt']/df['Total'])*100
df.to_csv('over_thirty.csv', header=True, index=None, mode='a')
