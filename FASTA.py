#!/usr/bin/env python3
# coding: utf-8

# In[7]:

import Bio
import pandas as pd
import numpy as np
from Bio.Seq import Seq

print("\n----------------------\n* Welcome to Sarah's FASTA program *\nThis script returns the top 10 most frequent sequence occurances in a fasta file. \nOutput is produced in csv format and saved in the script's folder.\nThe csv has the following information: sequence, length, count of occurances in fasta.\n-----------------------\n")
#define file being used
user_input = input("FASTA path/file please: ")

from Bio import SeqIO
records = list(SeqIO.parse(user_input, "fasta"))

#add sequence and id to empty lists
sequ = []
ids = []
for i in range(len(records)):
    sequ.append(records[i].seq)
    ids.append(records[i].id)

#create data frame with information
df = pd.DataFrame(ids, columns=['IDS'])
df['Sequence'] = sequ
df['Length'] = df['Sequence'].apply(lambda x: len(df['Sequence'][x]))

#iterate over dataframe and return counts of sequence occurances
sl = []
for i in range(len(df.index)):
    nt = df[df['Length'] == df['Length'][i]]
    same = nt[nt['Sequence'] == df['Sequence'][i]]
    sl.append(len(same.index))

#add count to dataframe
df['Count'] = sl

#sort dataframe based on count
result = df.sort(['Count'], ascending=False)

#drop IDS, might be import for something else but not needed here
result = result.drop('IDS', axis=1)

#drop duplicate rows
results = result.drop_duplicates()

#length and count for top 10 seq occurances
topten = results.head(10)

#write to csv
topten.to_csv('top_ten_count.csv', header=True, index=None, mode='a')


# In[ ]:
