#!/usr/bin/env python3
# coding: utf-8

import os
from Bio import SeqIO
import pandas as pd

di = input('Can you kindly drag the folder directory into the prompt?')

file_names_path = []
file_names = []
total = []
num_over_thirty = []
over_thirty = pd.DataFrame()



def find_name(folder):
    """
    This function takes in a folder location and searches through that location
    for fastq files. Once found the file and file path is split and the name is
    bumped into a list and then into a dataframe.
    """

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".fastq"):
                file_names_path.append(os.path.join(root, file))
                last_slash = file.split("/")[-1]
                name = last_slash.split(".")[0]
                file_names.append(name)
    over_thirty['File Name'] = file_names



def parse_fastq_file(path):
    for fastq_file in file_names_path:

        #parse files into a list of sequence records
        records = list(SeqIO.parse(fastq_file, "fastq"))

        #append total number or records in each file to a list
        record_num = len(records)
        total.append(record_num)

        #find all records for each file over length of 30nt append to list
        num_count = 0
        for i in range(len(records)):
            if len(records[i].seq) >= 30:
                num_count += 1
        num_over_thirty.append(num_count)


def calculate_over_30_per(total_seq, over_thirty_total):
    """
    This function adds total and total seq over 30 to a dataframe
    and calculates the rounded percent for seq over 30.
    """
    over_thirty['Total Count'] = total_seq
    over_thirty['Count over Thirty'] = over_thirty_total
    over_thirty['Percent of Seq Over 30nt'] = round((over_thirty['Count over Thirty']/over_thirty['Total Count'])*100)



find_name(di)
parse_fastq_file(file_names_path)
calculate_over_30_per(total, num_over_thirty)

#drop unneeded coulmns
over_thirty.drop(['Total Count','Count over Thirty'], axis=1, inplace=True)

#print dataframe of file name and Percent of Seq over 30nt
print(over_thirty)
