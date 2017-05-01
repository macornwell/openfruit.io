#!/bin/bash

database=$1

declare -a geotables=('geography_continent' 'geography_geocoordinate' 'geography_country' 'geography_zipcode' 'geography_state' 'geography_location' 'geography_city');
for table in "${geotables[@]}"
do
    echo Dumping ${table};
    sqlite3 ${database} ".dump ${table}" > openfruit/geography/sql/${table}.sql
done
