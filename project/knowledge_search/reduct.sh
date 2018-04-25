#1 info system
#2 features

./equivalence.sh $1 $2 > $1_$2

./dmatrix.sh $1_$2 $1 $2 | awk '{print $3}' | grep -v ^$ > $1_$2_d

./product.sh $1_$2_d | ./reduct_1.py  | sort -u | ./reduct_2.py | sort -r |  ./reduct_2.py
