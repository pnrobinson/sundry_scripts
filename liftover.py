import tempfile 
import sys
import os

LIFTOVER='/home/peter/IdeaProjects/svann/scripts/liftOver'
CHAIN='/home/peter/IdeaProjects/svann/scripts/hg19ToHg38.over.chain.gz'


if len (sys.argv) != 2:
    raise ValueError("Usage python liftover chr10:127460915-127466819")

posstring = sys.argv[1]
fields = posstring.strip().split(":")
if len(fields) != 2:
    raise ValueError("Malformed chrom-pos string:" + fields)
chrom = fields[0]
fields = fields[1].split("-")
if len(fields) != 2:
    raise ValueError("Malformed chrom-pos string:" + fields)
begin = int(fields[0])
end = int(fields[1])


bedfilename = "temp.txt"
temp = open(bedfilename, 'wt')


try:
    temp.writelines("%s\t%d\t%d" % (chrom, begin, end))
finally:
    temp.close() 


output_BED4 = "hg38coords.bed"
liftover_command = "%s %s %s %s unlifted.bed" % (LIFTOVER, bedfilename, CHAIN, output_BED4)
result = os.system(liftover_command)
if result != 0:
    print("[ERROR] Could not execute liftover: ", liftover_command)


hg38posstring = ""

with open(output_BED4) as f:
    for line in f:
        fields = line.strip().split("\t")
        if len(fields) != 3:
            raise ValueError("Malformed liftover string:" + fields)
        hg38posstring = "%s:%s-%s" % (fields[0],fields[1],fields[2] )


print("[INFO] hg37: ", posstring)
print("[INFO] hg38: ", hg38posstring)

