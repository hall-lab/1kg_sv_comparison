FROM ubuntu:16.04
MAINTAINER Dave Larson <delarson@wustl.edu>

# Volumes
# VOLUME /build
# VOLUME /release

# bootstrap build dependencies
RUN apt-get update -qq && \
    apt-get -y install apt-transport-https && \
    apt-get update -qq && \
    apt-get -y install \
    build-essential \
    bzip2 \
    libcurl4-openssl-dev \
    ca-certificates \
    libncurses5 \
    curl \
    zlib1g \
    zlib1g-dev \
    python \
    python-dev \
    python-pip \
    --no-install-recommends \ 
    && rm -rf /var/lib/apt/lists/*

# BCFTOOLS
RUN BCFTOOLS_VERSION=1.3.1 \
    && curl -LO https://github.com/samtools/bcftools/releases/download/${BCFTOOLS_VERSION}/bcftools-${BCFTOOLS_VERSION}.tar.bz2 \
    && tar -jxvf bcftools-${BCFTOOLS_VERSION}.tar.bz2 \
    && cd bcftools-${BCFTOOLS_VERSION} \
    && LIBS="-lcurl -lcrypto -lssl" make all \
    && make install \
    && cd htslib-${BCFTOOLS_VERSION} \
    && make install \
    && cd .. \
    && rm -rf bcftools-${BCFTOOLS_VERSION} \
    && rm -f bcftools-${BCFTOOLS_VERSION}.tar.bz2
# BEDTOOLS
RUN BEDTOOLS_VERSION=2.23.0 \
    && curl -LO https://github.com/arq5x/bedtools2/releases/download/v${BEDTOOLS_VERSION}/bedtools-${BEDTOOLS_VERSION}.tar.gz \
    && tar -xzvf bedtools-${BEDTOOLS_VERSION}.tar.gz \
    && cd bedtools2 \
    && make all \
    && make install \
    && cd .. \
    && rm -rf bedtools2 bedtools-${BEDTOOLS_VERSION}.tar.gz

# SVTOOLS
RUN pip install setuptools \
    && pip install pysam==0.8.4 svtools==0.3.1 pyVCF

CMD [ "/bin/bash" ]
