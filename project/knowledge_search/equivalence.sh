#1 table
#2 attributes

./product.sh $1 | ./equivalence.py $2 | sort -u
