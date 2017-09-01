ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz:
	curl -O ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/integrated_sv_map/ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz

ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.vcf.gz: ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz
	python 1kg_phase3_to_svtools_compat_svtype.py ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz | bgzip -c > ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.vcf.gz

ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.no_ins_of_mei.vcf.gz: ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.vcf.gz
	bcftools view ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.vcf.gz -e 'SVTYPE=="ALU" || SVTYPE=="LINE1" || SVTYPE=="SVA"' | bgzip -c > ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.no_ins_of_mei.vcf.gz

ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.non_rd_only.no_ins_of_mei.vcf.gz: ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.no_ins_of_mei.vcf.gz
	python remove_read_depth_only.py ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.no_ins_of_mei.vcf.gz | bgzip -c > ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.non_rd_only.no_ins_of_mei.vcf.gz

.PHONY: all

all: ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.svtools_types.non_rd_only.no_ins_of_mei.vcf.gz
