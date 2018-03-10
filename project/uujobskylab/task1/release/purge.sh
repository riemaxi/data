bgzip -dc $1.gz | grep -ve ^# | ./purge.py $2 | ./header.py | bgzip > purged.$1.gz

tabix -f -p vcf purged.$1.gz
