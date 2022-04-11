#!/bin/sh
#sleep 5
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
python app.py runserver 0.0.0.0:5000
