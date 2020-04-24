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

### getting coverage with Samtools
* First have to align the quality filtered reads to the assembly
* using [bowtie2] [1]: http://bowtie-bio.sourceforge.net/bowtie2/index.shtml


### Cut-offs for contigs
* No right answer
* For a single isolate genome assembly, min of 5x or 10x coverage and contig length > 1000-2000 bp


