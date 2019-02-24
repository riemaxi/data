cat align.txt.random | sort -rn | awk -F $"\t" '{print $2,",",$3}' > align.txt
