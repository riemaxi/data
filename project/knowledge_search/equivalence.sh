#1 table
#2 attributes

./product.sh $1 | ./discern.py $2 | sort | ./equivalence.py
