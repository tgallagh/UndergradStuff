# Checking genome assembly

### common assembly parameters
* N50=length of contig that is 50% of total genome length
* Number of contigs
* Total number of bases
* Shortest contig
* Longest contig
* Average contig length
* typically provided in the assembler output of summary stats or log
* example: A5, megaHit
	* for ex, can look at the last couple of lines of megahit log
		> STAT] 138 contigs, total 6554082 bp, min 222 bp, max 687872 bp, avg 47493 bp, N50 292911 bp
* Note, spades does not give assembly stats and recommends QUAST to assess assembly quality
* Another useful parameter is coverage:
	* Number of unique reads that align to a given nucleotide in the contig or genome
	* We can calculate the average coverage across a contig: 
		> SUM of aligned reads / length of contig
	* typically want the coverage to be the same across a contig
	* some examples where you may get different coverages:
		* repeat regions might have higher coverage
	* most aligners don't automatically generate this stat

### getting coverage with Samtools and bedtools
# First have to align the quality filtered reads to the assembly
* for ex using [bowtie2]:

[bowtie2]: http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
Have to first index your reference genome (your assemblies) <br />
```
module load bowtie2/2.2.7
bowtie2-build <INPUT GENOME ASSEMBLY> <ENTER REF PREFIX>

```
Then can do a quick alignment of QF reads to the indexed genome <br />

```
bowtie2 --very-fast -x  <INPUT PATH TO YOUR REF PREFIX> \n
	-1 <INPUT PATH TO QF READ1>
	-2 <INPUT PATH TO QF READ2>
	-S <DEST PATH OF SAM FILE>
```
bowtie2 will give an output SAM file, which lists the location of read mappings to your genome and some other alignment STATS <br />

# then can use [samtools] to convert SAM to BAM (binary version) and sort
```
module load samtools
samtools view -bS <PATH TO SAM FILE> | samtools sort > <DEST OF SORTED BAM FILE>
```
[samtools]: http://samtools.sourceforge.net/

# [bedtools] can calculate a histogram of genome coverage
```
module load bedtools
bedtools genomecov -i <BAM FILE> -g <GENOME FILE>
```

### putting parameters in one file 

### Cut-offs for contigs
* No right answer
* For a single isolate genome assembly, min of 5x or 10x coverage and contig length > 1000-2000 bp
in progress...


