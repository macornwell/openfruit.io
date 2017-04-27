#!/bin/bash
echo 'migrate';
./manage.py migrate;
echo 'setup_groups';
./manage.py setup_groups;
echo 'setup_default_taxonomy';
./manage.py setup_default_taxonomy;
