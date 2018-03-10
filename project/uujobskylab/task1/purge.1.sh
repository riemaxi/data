bgzip -dc $1.gz | ./purge.py $2 | ./header.py > purged.$1

bgzip purged.$1

tabix -p vcf purged.$1.gz
