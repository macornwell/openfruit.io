#!/usr/bin/env bash
if [ -f ./db.sqlite3 ]
then
    echo "Deleting old database";
    rm ./db.sqlite3;
fi
./setup_script.sh
echo "Inserting Debug Data";
source $HOME/dev/env/openfruit/bin/activate;
python ./insert_debug_data.py
