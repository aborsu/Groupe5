nlines=$(wc -l ftb6_2.mrg | cut -f 1 | grep -P "[0-9]* " -o)
let "nlines = (nlines/10)*9"
split ftb6_2.mrg -l $nlines ftb_ -d
cat ftb_01|tr "\n" "@"|grep -o -P " [^)^(]+\)+@?"|grep -o -P "[^)]+"|tr "\n" " "|sed 's/  / /g'|sed 's/ @ /\n/g'|tr "@" "\n"
