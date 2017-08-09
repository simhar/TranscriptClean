
from transcript import Transcript
from spliceJunction import SpliceJunction
from optparse import OptionParser
import pybedtools
from pyfasta import Fasta

def getOptions():
    parser = OptionParser()
    parser.add_option("--f", dest = "sam", help = "Input file",
                      metavar = "FILE", type = "string", default = "")
    parser.add_option("--g", dest = "refGenome", help = "Reference genome fasta file. Should be the same one used to generate the sam file.",
                      metavar = "FILE", type = "string", default = "")
    parser.add_option("--s", dest = "spliceAnnot", help = "Splice junction file obtained by mapping Illumina reads to the genome using STAR. More formats may be supported in the future.",
                      metavar = "FILE", type = "string", default = "")
    parser.add_option("--o", dest = "outfile",
                      help = "output file", metavar = "FILE", type = "string", default = "out")
    (options, args) = parser.parse_args()
    return options

def main():
    options = getOptions()
   
    # Read in the reference genome. Treat coordinates as 0-based 
    genome = Fasta(options.refGenome)
    header, transcripts = processSAM(options.sam, genome)
    annotatedSpliceJns = processSpliceAnnotation(options.spliceAnnot)
    

def processSAM(sam, genome):
    # This function extracts the SAM header (because we'll need that later) and creates a Transcript object for every sam transcript. 
    # Transcripts are returned in a list. 

    header = ""
    transcripts = []
    with open(sam, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("@"):
                header = header + line + "\n"
                continue
            t = Transcript(line, genome)
            transcripts.append(t)
    return header, transcripts

def processSpliceAnnotation(annotFile):
    # This function reads in the tab-separated STAR splice junction file and creates a bedtools object
    
    bedstr = ""
    with open(annotFile, r) as f:
        for line in f:
            line = line.strip()
        

main()
