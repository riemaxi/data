cat dalign.txt.random | sort -rn | awk -F $"\t" '{print $2,",",$3}' > dalign.txt
