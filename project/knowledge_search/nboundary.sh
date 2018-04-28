#1 data
#2 start code
#3 column
#4 field separator
#5 arity

cat $1 | ./nominal.py $2 $3 $4 | ./nboundary.py $4 $5
