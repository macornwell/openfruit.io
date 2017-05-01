#!/usr/bin/env bash
#cat openfruit/geography/processed_geo.sql | sqlite3 db.sqlite3

database=$1

declare -a geotables=('geography_continent' 'geography_geocoordinate' 'geography_country' 'geography_zipcode' 'geography_state' 'geography_location' 'geography_city');
# Drop Geo Tables
for table in "${geotables[@]}"
do
	echo Dropping ${table};
	sqlite3 ${database} "drop table ${table}";
done

# Insert Geo Tables#!/usr/bin/env bash
for table in "${geotables[@]}"
do
    echo Inserting ${table};
    cat "openfruit/geography/sql/${table}.sql" | sqlite3 ${database}
done
#sqlite3 ./db.sqlite3 '.dump geography_continent' > 1.sql
