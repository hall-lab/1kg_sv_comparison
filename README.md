# 1kg_sv_comparison
Scripts utilized to prep data for comparison of calls from the svtools pipeline to calls from the 1000 Genomes Project. This code is specific for the 1000 Genomes Phase 3 Integrated SV Map currently found here: ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/integrated_sv_map/ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz

# Dependencies
* curl
* Python (2.7)
* PyVCF (0.6.8)
* pysam (0.8.4)
* bgzip (any version)
* bcftools (>=1.2)
* make (if you use the Makefile)

# 1000 Genome Calls Preparation
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
4. Remove SV calls only detected by readdepth based algorithms.
   ```
   python remove_read_depth_only.py \
      ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.no_ins_of_mei.vcf.gz \
      | bgzip -c \
      > ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.non_rd_only.no_ins_of_mei.vcf.gz
   ```
