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

bowtie2 -x <PATH TO DESIRED OUTPUT DIRECTORY AND PREFIX> \
 -1 $input\READ1.fastq -2 $input\READ2.fastq \ 
 -S <DESIRED DIRECTORY AND NAME OF ALIGNMENT OUTPUT>

```

Here is an example using Amanda and Clark's coevolution reads.
Bowtie2 requires an index of the reference genome to do alignments. 
You should do the bowtie2-build step beforehand interactively or in a submitted job (otherwise, this step will be repeated in all tasks in the job array)

The job array is going to align the PE reads from 15 samples to the PA14 genome. 
Here are the names of the 15 samples:  
12C_598_1  
12C_598_2  
12C_598_3  
12C_598_4  
12P_598_1  
12P_598_2  
12P_598_3  
12P_598_4  
9C_598_2  
9C_598_3  
9C_598_4  
9P_598_1
9P_598_2
9P_598_3
9P_598_4

How do we make a filename.txt file with just the prefixes? The directory with the READ1 and READ2 files also has other PE fastq files (592 phage files) we don't want to include in this job array.
We only want the 598 phage files. 

```
# this is a kinda awful way to make the file, but it works
# cd into the directory in an I/O node 
for i in *598_[0-9].read1_paired.fastq; \
do echo $i >> filenames.txt ; done

# check the text file
cat filenames.txt

# and can check to make sure only 15 samples
cat filenames.txt | wc -l

# but we only want prefixes for job arrays with PE reads as input
# use sed to remove the suffixes
sed -i "s/".read1_paired.fastq"//g" filenames.txt

#and then double check that we only have prefixes like what's listed above
cat filenames.txt
```

And now we can make the script to run a job array.

```
#!/bin/bash
#$ -N Phage598Align
#$ -t 1-15 

module load bowtie2/2.2.7

# filenames.txt contains list of filename prefixes 
input=$(head -n $SGE_TASK_ID filenames.txt | tail -n 1)

# build reference genome index 
REF=/path/to/directory/with/index/
DEST=/path/to/desired/output/directory/

# should build a reference index beforehand:
# bowtie2-build pa14_rga_withn.fasta $REF/pa14

bowtie2 -x $REF \
 -1 $input\.read1_paired.fastq -2 $input\.read2_paired.fastq \ 
 -S $DEST$input.sam 

```

