cat $1 | sed 's/^{{/{/g' > $1.nw
mv $1.nw $1

