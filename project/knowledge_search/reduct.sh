#1 classes
#2 info system
#3 features

./dmatrix.sh $1 $2 $3 | awk '{print $3}' | grep -v ^$ > $1_d

./product.sh $1_d | ./reduct_1.py  | sort -u | ./reduct_2.py | sort -r |  ./reduct_2.py
