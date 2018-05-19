# 1 source
# 2 size
# 3 starting base
# 4 ending base
# 5 destination

./fragment.sh $1 $2 $3 $4 | ./stairify.py $2 $5
