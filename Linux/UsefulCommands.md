# Useful bash one-liners for working with sequencing data


Convert a multi-line fasta to a single-line fasta:
```
awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < INFILE | tail -n +2 > OUTFILE
```

Print headers of a fasta file:
```
grep  "^>" INFILE
```
