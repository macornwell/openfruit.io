#!/bin/bash
source $HOME/dev/env/openfruit/bin/activate;

echo 'makemigrations'
./manage.py makemigrations;
echo 'migrate';
./manage.py migrate;
echo 'setup_groups';
./manage.py setup_groups;
echo 'setup_default_taxonomy';
./manage.py setup_default_taxonomy;
echo 'Setting up Events';
./manage.py setup_events;
echo 'Setting up Geo Data';
./drop_then_add_geo.sh $HOME/dev/env/openfruit/lib/python3.4/site-packages/django_geo_db/sql/ db.sqlite3
