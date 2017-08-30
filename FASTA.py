#!/usr/bin/env python3
# coding: utf-8

from Bio import SeqIO
import pandas as pd

user_input = input('Could you kindly drag your FASTA file of interest into the consol?')
records = list(SeqIO.parse(user_input, "fasta"))

seq_list = []
df = pd.DataFrame()

def add_seq_to_dataframe(folder_file):
    """
    This function takes in a paresed fasta file and interates over the records
    in that file with the attribute seq. These sequences are bumped into a list
    The list is assigned to an empty dataframe with a column called Sequence
    """
    for i in range(len(records)):
        seq_list.append(str(records[i].seq))
    df['Sequence'] = seq_list



count = []
seq = []
df_seq = pd.DataFrame()

def unique_seq(df):
    """
    This function takes in a dataframe of sequences. It then find the unique
    sequences within the dataframe and addes each to a list. All sequences that
    match the unique sequence are bumped into a dataframe (ref_seq) and the
    number of rows are counted and bumped into the list count. The unque Seq
    and the count is then placed into a new dataframe (df_seq)
    """
    uniq_seq = list(df['Sequence'].unique())
    for i in range(len(uniq_seq)):
        ref_seq = df[df['Sequence'] == uniq_seq[i]]
        seq.append(uniq_seq[i])
        count.append(len(ref_seq))
    df_seq['Seq'] = seq
    df_seq['Count'] = count
    df_seq.sort(['Count'], inplace=True, ascending=False)

add_seq_to_dataframe(user_input)
unique_seq(df)

print(df_seq.head(20))
