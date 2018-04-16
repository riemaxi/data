cat $1 | awk '{print NR","$0}' > $1_index
