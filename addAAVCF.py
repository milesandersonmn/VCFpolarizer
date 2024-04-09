import pysam

fileName = "../VCFs/Schil_capture_variants_AllChroms.decomposedVariants.filtered.maxMissing.sorted.SNPs.vcf.gz"

myvcf = pysam.VariantFile(fileName, "r")

myvcf.header.info.add("AA", "1", "String", "Ancestral Allele")

vcf_out = pysam.VariantFile('out.vcf', 'w', header=myvcf.header)