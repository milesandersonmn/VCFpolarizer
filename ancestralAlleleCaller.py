#!/usr/bin/env python

import sys
import gzip
import argparse
import logging

#script adds ancestral allele field (AA) based on outgroup sample that is called in a multi-sample VCF.
#If outgroup is heterozygous or missing, SNP position is skipped.




logging.basicConfig(level=logging.INFO)

def main(args):
    # Open the VCF files
    zipped = args.input_vcf.endswith(".gz")
    vcf = gzip.open(args.input_vcf, "rt") if zipped else open(args.input_vcf, "r")
    out = gzip.open(args.output_vcf, "wt") if zipped else open(args.output_vcf, "w")

    try:
        for line in vcf:
            if line[0] == "#":
                if line[1] != "#":
                    header = line.rstrip().split("\t")
                    try:
                        outidx = header.index(args.outgroup)
                    except ValueError:
                        logging.error(f"Outgroup {args.outgroup} not found in VCF header.")
                        sys.exit(1)
                out.write(line)
                continue

            line = line.rstrip().split("\t")
            outallele = line[outidx].split(":")[0]
            if outallele in {".", "./.", "0/1", "1/0", "0|1", "1|0", ".|."}:
                continue
            elif outallele in {"0/0", "0|0"}:
                anc = "AA=" + line[3]
                info = anc + ";" + line[7]
                line[7] = info
                out.write("\t".join(line) + "\n")
            elif outallele in {"1/1", "1|1"}:
                anc = "AA=" + line[4]
                info = anc + ";" + line[7]
                line[7] = info
                out.write("\t".join(line) + "\n")
            else:
                logging.error(f"Unknown allelic state in outgroup: {outallele}")
                sys.exit(1)
    finally:
        vcf.close()
        out.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Polarize a VCF file by an outgroup.')
    parser.add_argument('input_vcf', help='Path to the input VCF file, can be gzipped.')
    parser.add_argument('outgroup', help='Name of the outgroup sample in the VCF file.')
    parser.add_argument('output_vcf', help='Path to the output VCF file.')
    args = parser.parse_args()

    main(args)