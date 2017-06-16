#!/usr/bin/env python3
# coding: utf-8

# In[153]:

from collections import defaultdict
import gzip
import pandas as pd
import re
import numpy as np

print("\n----------------------\n* Welcome to Sarah's Gene Finder program *\nThis script parses a GTF file and txt file containing:\n(Tab-delimited file: Chr<tab>Position)\nIt then uses the GTF file to locate the gene present given at the txt file coordinates.\nThis program then saves the results in a csv within the script's folder.\n\nThe csv includes:\nChormosome number, Location, Gene (if one was found)\n-----------------------\n")


#path of annotated file
annotated = input("txt palth/file please: ")
annotated.rstrip()

#path of gtf file
gtf_file = input("gtf path/file please: ")
gtf_file.rstrip()

#parser from github: https://gist.github.com/slowkow/8101481
GTF_HEADER  = ['seqname', 'source', 'feature', 'start', 'end', 'score',
               'strand', 'frame']
R_SEMICOLON = re.compile(r'\s*;\s*')
R_COMMA     = re.compile(r'\s*,\s*')
R_KEYVALUE  = re.compile(r'(\s+|\s*=\s*)')


def dataframe(filename):
    """Open an optionally gzipped GTF file and return a pandas.DataFrame.
    """
    # Each column is a list stored as a value in this dict.
    result = defaultdict(list)

    for i, line in enumerate(lines(filename)):
        for key in line.keys():
            # This key has not been seen yet, so set it to None for all
            # previous lines.
            if key not in result:
                result[key] = [None] * i

        # Ensure this row has some value for each column.
        for key in result.keys():
            result[key].append(line.get(key, None))

    return pd.DataFrame(result)


def lines(filename):
    """Open an optionally gzipped GTF file and generate a dict for each line.
    """
    fn_open = gzip.open if filename.endswith('.gz') else open

    with fn_open(filename) as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            else:
                yield parse(line)


def parse(line):
    """Parse a single GTF line and return a dict.
    """
    result = {}

    fields = line.rstrip().split('\t')

    for i, col in enumerate(GTF_HEADER):
        result[col] = _get_value(fields[i])

    # INFO field consists of "key1=value;key2=value;...".
    infos = re.split(R_SEMICOLON, fields[8])

    for i, info in enumerate(infos, 1):
        # It should be key="value".
        try:
            key, _, value = re.split(R_KEYVALUE, info)
        # But sometimes it is just "value".
        except ValueError:
            key = 'INFO{}'.format(i)
            value = info
        # Ignore the field if there is no value.
        if value:
            result[key] = _get_value(value)

    return result


def _get_value(value):
    if not value:
        return None

    # Strip double and single quotes.
    value = value.strip('"\'')

    # Return a list if the value has a comma.
    if ',' in value:
        value = re.split(R_COMMA, value)
    # These values are equivalent to None.
    elif value in ['', '.', 'NA']:
        return None

    return value

#conver GTF file to dataframe
df = dataframe(gtf_file)
df['start'] = df['start'].apply(lambda x: int(x))
df['end'] = df['end'].apply(lambda x: int(x))

#convert annotated file to dataframe
dft = pd.read_table(annotated, names=['chr', 'num'])

#iterate over GTF dataframe filtering by row in annotated data frame
gene = []
for i in range(len(dft)):
    df_new = df[(df['seqname'] == dft['chr'][i]) & (df['start'] <= dft['num'][i]) & (df['end'] >= dft['num'][i])]
    if (len(df_new.index) < 1):
        gene.append('NA')
    else:
        l = list(df_new['gene_name'])
        gene.append(l[0])

#adding to annotated dataframe, gene name
dft['Name'] = gene
dft.to_csv('gene.csv', header=True, index=None, mode='a')
