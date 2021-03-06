# Checking genome assembly

### common assembly parameters
* N50 is the length of the smallest contig in the set that contains the fewest (largest) contigs whose combined length represents at least 50% of the assembly
* L50 is the number of contigs whose summed length is N50
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
	-1 <INPUT PATH TO QF READ1> \n
	-2 <INPUT PATH TO QF READ2> \n
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
* to use bedtools genomecov, must first generate a .genome file
* can use bash functions to do this
```
cat <INPUT ASSEMBLY FILE>  | grep "^>" | sed 's/flag.*len=//' | sed 's/>//' | sed 's/ /\t/g' > <SAMPLE NAME>.genome 
```

```
module load bedtools
bedtools genomecov -i <BAM FILE> -g <GENOME FILE> > <DEST PATH OF .TXT>
```
[bedtools]:https://bedtools.readthedocs.io/en/latest/content/tools/genomecov.html

* can also pipe samtools output into bedtools
* for ex:
```
cd /dfs5/bio/tgallagh/Wound_Sputum_RawSeq/data/processed/megahit
for i in $(ls); do echo $i & samtools view -b $i/bowtie2/$i.bam | genomeCoverageBed -ibam stdin -g $i/cdhit/$i.genome > $i/cdhit/$i\_bedcoverage.txt ; done
```

### putting parameters in one file 

### Cut-offs for contigs
* No right answer
* For a single isolate genome assembly, min of 5x or 10x coverage and contig length > 1000-2000 bp
in progress...


