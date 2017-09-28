# Job array with paired end sequencing files

Guide to HPC Bio que: https://hpc.oit.uci.edu/~krthornt/BioClusterGE.pdf 

Here is a skeleton script for aligning paired end sequencing reads as a job array. 


```
#!/bin/bash
#$ -N <INSERT JOBNAME>
#$ -t <1-INSERT NUMBER OF SAMPLES>

module load bowtie2/2.2.7

# filenames.txt contains list of filename prefixes 
input=$(head -n $SGE_TASK_ID filenames.txt | tail -n 1)

# build reference genome index 
bowtie2-build <PATH AND FILE NAME OF GENOME ASSEMBLY> <PATH TO DESIRED OUTPUT DIRECTORY AND PREFIX>

bowtie2 -x <PATH TO DESIRED OUTPUT DIRECTORY AND PREFIX> \
 -1 $input\READ1.fastq -2 $input\READ2.fastq \ 
 -S <DESIRED DIRECTORY AND NAME OF ALIGNMENT OUTPUT>

```

Here is an example using Amanda and Clark's coevolution reads. 

```
#!/bin/bash
#$ -N <INSERT JOBNAME>
#$ -t <1-INSERT NUMBER OF SAMPLES>

module load bowtie2/2.2.7

# filenames.txt contains list of filename prefixes 
input=$(head -n $SGE_TASK_ID filenames.txt | tail -n 1)

# build reference genome index 
REF=/path/to/directory/with/index/
DEST=/path/to/desired/output/directory/

bowtie2-build pa14_rga_withn.fasta $REF/pa14

bowtie2 -x <PATH TO DESIRED OUTPUT DIRECTORY AND PREFIX> \
 -1 $input\.read1_paired.fastq -2 $input\.read2_paired.fastq \ 
 -S $DEST$input.sam 

```

