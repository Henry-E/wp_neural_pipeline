for file_name in translate/eval*/*detok.tc
do
	tr '\n' ' ' < "$file_name" > "$file_name".one_line
	sed 's/ Break\s*/\n/g' "$file_name".one_line > "$file_name".utts
done
	
