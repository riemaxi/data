#1 data
#2 start code
#3 column
#4 sep
#5 arity

./boundary.sh  data/iris 1 4 , 5 | awk '{print $2 - $1}' | sort | head -n 1
