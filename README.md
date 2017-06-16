# python_bioinformatics_tools

<h1>Tools</h1>
<p>This folder contains three bioinformatics tools built using python3. These programs can be run on the command line and should prompt the user for appropriate information</p>
<h3>FASTQ</h3>
<p>The FASTQ program with search through a given folder path and find all '.fastq' files located within that folder. It will then return a csv of: fastq file names, file path, total sequences count, total sequence count over 30nt, percent of sequences over 30nt long. This file is then saved in the folder the program resides in</p>
<h3>FASTA</h3>
<p>The FASTA program searches a '.fasta' file for the top ten most frequent seqences within the file. It then returns a csv with: the sequence, the length of the squence, the number of times it occured within the file. This file is then saved in the folder the program resides in</p>
<h3>Chromosome</h3>
<p>The Chromosome program takes two files. The first is a tab deliminated '.txt' file giving a chromosome and position within that chromosome. It also takes in a '.GTF' file with genomic annotations. Using the txt file input it looks up the corresponding gene at that location within the GTF file. The program returns a csv containing the chromosome and location within the txt file as well as coresponding gene at that location. This file is then saved in the folder the program resides in.</p>
