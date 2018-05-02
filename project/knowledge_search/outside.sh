#1 classes
#2 info
#3 sep
#4 concept

cat $1 | ./outside.py $2 $3 $4 | sort -n -u
