#!/bin/bash
echo 'migrate';
./manage.py migrate;
echo 'setup_groups';
./manage.py setup_groups;
echo 'setup_default_taxonomy';
./manage.py setup_default_taxonomy;
echo 'Setting up Events';
./manage.py setup_events;
echo 'Setting up Geo Data';
cat openfruit/geography/processed_geo.sql | sqlite3 db.sqlite3 
