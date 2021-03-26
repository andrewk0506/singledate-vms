#!/usr/bin/env bash

python3 manage.py migrate

echo "server running at port 8000"
python3 manage.py runserver 0.0.0.0:8000

