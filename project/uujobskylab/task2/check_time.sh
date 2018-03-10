#initialize period, shift and h

shft=0
period=3

h=$(date +%-H)

# set the every 3 hours flag
((z = (h+shft) % period))

# test the flag
if [ $z != 0 ]; then
 /bin/false
fi
