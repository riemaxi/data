# 1 source
# 2 size
# 3 starting base
# 4 number of bases

tr -d '\n' < $1 | ./fragment.py $2 $4 | tail -n +$3
