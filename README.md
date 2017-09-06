# 1kg_sv_comparison
Scripts utilized to prep data for comparison of calls from the svtools pipeline to calls from the 1000 Genomes Project. This code is specific for the 1000 Genomes Phase 3 Integrated SV Map currently found here: ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/integrated_sv_map/ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz

# Dependencies
* curl
* Python (2.7)
* PyVCF (0.6.8)
* pysam (0.8.4)
* bgzip (any version)
* bcftools (>=1.2)
* svtools (>=0.3.1)
* perl (>=0.5.10)
* make (if you use the Makefile)

# 1000 Genome Calls Preparation
A Makefile is provide to run these steps. If the dependencies are met then you can run by typing `make all`.
1. Download the calls
   ```
   curl -O ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/integrated_sv_map/ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz
   ```
2. Convert to svtools/lumpy-sv compatible SVTYPE fields.
   ```
   python 1kg_phase3_to_svtools_compat_svtype.py \
      ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz \
      | bgzip -c > ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.vcf.gz
   ```
3. Remove MEI insertions (relative to the reference)
   * These aren't compatible with svtools as they lack an END INFO field and the pipeline doesn't detect these.
   ```
   bcftools view -e 'SVTYPE=="ALU" || SVTYPE=="LINE1" || SVTYPE=="SVA"' \
      ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.vcf.gz - \
      | bgzip -c > ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.no_ins_of_mei.vcf.gz
   ```
4. Remove SV calls only detected by read depth based algorithms.
   ```
   python remove_read_depth_only.py \
      ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.no_ins_of_mei.vcf.gz \
      | bgzip -c \
      > ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.non_rd_only.no_ins_of_mei.vcf.gz
   ```
# Comparison of SV VCF to 1000 Genomes
A wrapper script is provided to aid in the comparison of multiple samples.
## Inputs
   1. The 1000 Genomes VCF prepared above.
   2. An evaluation VCF containing samples overlapping with the 1000 Genomes cohort.
   3. A 2-column, tab-separated file where the first column is the sample name in the evaluation VCF and the second column is the sample name in the 1000 Genomes VCF. For example:
      ``` 
      H_IJ-NA19239-NA19239_B9	NA19239
      ```
## Invocation
The script is called like:
```
bash 1kg_sens_multi.sh \
   ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.non_rd_only.no_ins_of_mei.vcf.gz \
   cohort.sv.gt.cn.pruned.reclassed.filtered.nosec.vcf.gz \
   sample_name_in_1kg.map
```

## Results
In the current working directory, a sub-directory for each 1000 Genomes sample is created. Inside each sub-directory will be three files.
   1. A BEDPE of the 1000 Genomes call for the sample.
   2. A BEDPE of the evaluation calls for the sample.
   3. A file of calculated sensitivities which has structure as shown below:
      ```
      Unfiltered Total Calls	9586
      Unfiltered Overlapping 1KG	1641
      Unfiltered Fraction Overlapping 1KG	0.171187
      Unfiltered 1KG Sensitivity	0.888949
      Filtered Total Calls	3916
      Filtered Overlapping 1KG	1559
      Filtered Fraction Overlapping 1KG	0.39811
      Filtered 1KG Sensitivity	0.844529
      ```
