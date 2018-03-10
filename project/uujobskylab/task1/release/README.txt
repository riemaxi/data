Description

The script is designed as a pipeline

bgzip -dc $1.gz | grep -ve ^# | ./purge.py $2 | ./header.py | bgzip > purged.$1.gz

where 
1- The content is sent to the console
2- The header is removed
3- purging process is carried out with a parameter as input. This parameter is the column from which the data will cut off
4- Because purge can not assume anything about the header, a custom heaer.py is provided which simply read a file header.cvf
header.cvf is provided by the user of the script
5- the purged content is bgzipped 
6- Finally the purged zipped content is indexed with tabix

It is recommended to install pysam by way of bioconda

Obs. samtools is picky about zipping files. bgzip is used instead of gzip


Usage

./purge.sh <bgziped vcf> <from>

Output

purged.<bgziped vcf>
purged.<bgziped vcf>.tbi

Exampe

./purge.sh sample.vcf.gz 9

Output

purged.sample.vcf.gz
purged.sample.vcf.gz.tbi
