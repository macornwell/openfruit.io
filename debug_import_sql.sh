#!/usr/bin/env bash
database=$1
folder=$2

echo $database
echo $folder

for file in $(find $folder -type f -maxdepth 1)
do
    if [[ -f $file ]]; then
    echo "$file"
    cp $file "$file".bak
    cat "$file".bak | sed -e 's/openfruit.//g' > $file
    sqlite3 $database < $file
    fi
done
